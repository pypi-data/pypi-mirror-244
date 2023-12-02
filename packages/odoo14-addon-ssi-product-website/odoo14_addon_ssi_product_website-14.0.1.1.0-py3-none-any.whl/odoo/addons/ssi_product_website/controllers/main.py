# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website.controllers.main import QueryURL

_logger = logging.getLogger(__name__)


class TableCompute(object):
    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(1, ppr)
            y = min(1, ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1
            # if 21st products (index 20) and the last line is full (ppr products in it), break
            # (pos + 1.0) / ppr is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:  # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                "product": p,
                "x": x,
                "y": y,
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows


class ProductWebsite(http.Controller):
    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        order = post.get("order") or "name ASC"
        return order

    def _get_search_domain(self, search, search_in_description=True):
        domains = [[("product_catalog", "=", True)]]
        if search:
            for srch in search.split(" "):
                subdomains = [
                    [("name", "ilike", srch)],
                    [("product_variant_ids.default_code", "ilike", srch)],
                ]
                if search_in_description:
                    subdomains.append([("description", "ilike", srch)])
                domains.append(expression.OR(subdomains))

        return expression.AND(domains)

    # TODO: flake8
    def sitemap_product_catalog(env, rule, qs):  # noqa: B902
        if not qs or qs.lower() in "/product_catalog":
            yield {"loc": "/product_catalog"}

    @http.route(
        [
            """/product_catalog""",
            """/product_catalog/page/<int:page>""",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_product_catalog,
    )
    def product_catalog(self, page=0, search="", ppg=False, **post):
        add_qty = int(post.get("add_qty", 1))

        if ppg:
            try:
                ppg = int(ppg)
                post["ppg"] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = 20

        ppr = 4

        attrib_list = request.httprequest.args.getlist("attrib")
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}

        domain = self._get_search_domain(search)

        keep = QueryURL("/product_catalog", search=search, order=post.get("order"))

        request.context = dict(request.context, partner=request.env.user.partner_id)

        url = "/product_catalog"
        if search:
            post["search"] = search

        Product = request.env["product.template"].with_context(bin_size=True)

        search_product = Product.search(domain, order=self._get_search_order(post))

        product_count = len(search_product)
        pager = request.website.pager(
            url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post
        )
        offset = pager["offset"]
        products = search_product[offset : offset + ppg]

        ProductAttribute = request.env["product.attribute"]
        if products:
            # get all products without limit
            attributes = ProductAttribute.search(
                [("product_tmpl_ids", "in", search_product.ids)]
            )
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = "grid"

        values = {
            "search": search,
            "order": post.get("order", ""),
            "pager": pager,
            "add_qty": add_qty,
            "products": products,
            "search_count": product_count,  # common for all searchbox
            "bins": TableCompute().process(products, ppg, ppr),
            "ppg": ppg,
            "ppr": ppr,
            "attributes": attributes,
            "keep": keep,
            "layout_mode": layout_mode,
        }
        return request.render("ssi_product_website.products", values)

    @http.route(
        ['/product_catalog/<model("product.template"):product>'],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def product(self, product, search="", **kwargs):
        if not product.product_catalog:
            raise NotFound()

        return request.render(
            "ssi_product_website.product",
            self._prepare_product_values(product, search, **kwargs),
        )

    def _prepare_product_values(self, product, search, **kwargs):
        add_qty = int(kwargs.get("add_qty", 1))

        # TODO: flake8
        product_context = dict(  # noqa: F841
            request.env.context,
            quantity=add_qty,
            active_id=product.id,
            partner=request.env.user.partner_id,
        )

        keep = QueryURL("/product_catalog", search=search)

        # Needed to trigger the recently viewed product rpc
        view_track = request.website.viewref("ssi_product_website.product").track

        return {
            "search": search,
            "keep": keep,
            "main_object": product,
            "product": product,
            "add_qty": add_qty,
            "view_track": view_track,
        }
