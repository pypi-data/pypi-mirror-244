# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.http_routing.models.ir_http import slug


class ProductTemplate(models.Model):
    _inherit = ["product.template", "website.seo.metadata"]
    _name = "product.template"
    _mail_post_access = "read"
    _check_company_auto = True

    def _compute_catalog_url(self):
        for product in self:
            if product.id:
                product.catalog_url = "/product_catalog/%s" % slug(product)

    catalog_url = fields.Char(string="Catalog URL", compute="_compute_catalog_url")
    product_catalog = fields.Boolean(
        string="Show in Product Catalog", default=True, required=False
    )

    def _get_combination_info_catalog(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        parent_combination=False,
        only_template=False,
    ):
        self.ensure_one()
        # get the name before the change of context to benefit from prefetch
        display_name = self.display_name

        display_image = True
        quantity = self.env.context.get("quantity", add_qty)
        context = dict(self.env.context, quantity=quantity)
        product_template = self.with_context(context)

        combination = (
            combination or product_template.env["product.template.attribute.value"]
        )

        if not product_id and not combination and not only_template:
            combination = product_template._get_first_possible_combination(
                parent_combination
            )

        if only_template:
            product = product_template.env["product.product"]
        elif product_id and not combination:
            product = product_template.env["product.product"].browse(product_id)
        else:
            product = product_template._get_variant_for_combination(combination)

        if product:
            # We need to add the price_extra for the attributes that are not
            # in the variant, typically those of type no_variant, but it is
            # possible that a no_variant attribute is still in a variant if
            # the type of the attribute has been changed after creation.
            no_variant_attributes_price_extra = [
                ptav.price_extra
                for ptav in combination.filtered(
                    lambda ptav: ptav.price_extra
                    and ptav not in product.product_template_attribute_value_ids
                )
            ]
            if no_variant_attributes_price_extra:
                product = product.with_context(
                    no_variant_attributes_price_extra=tuple(
                        no_variant_attributes_price_extra
                    )
                )
            list_price = product.price_compute("list_price")[product.id]
            price = list_price
            display_image = bool(product.image_128)
            display_name = product.display_name
            price_extra = (product.price_extra or 0.0) + (
                sum(no_variant_attributes_price_extra) or 0.0
            )
        else:
            current_attributes_price_extra = [v.price_extra or 0.0 for v in combination]
            product_template = product_template.with_context(
                current_attributes_price_extra=current_attributes_price_extra
            )
            price_extra = sum(current_attributes_price_extra)
            list_price = product_template.price_compute("list_price")[
                product_template.id
            ]
            price = list_price
            display_image = bool(product_template.image_128)

            combination_name = combination._get_combination_name()
            if combination_name:
                display_name = "%s (%s)" % (display_name, combination_name)

        combination_info = {
            "product_id": product.id,
            "product_template_id": product_template.id,
            "currency_id": product_template.currency_id,
            "display_name": display_name,
            "display_image": display_image,
            "price": price,
            "list_price": list_price,
            "price_extra": price_extra,
        }

        if self.env.context.get("website_id"):
            current_website = self.env["website"].browse(self.env.context["website_id"])
            partner = self.env.user.partner_id
            company_id = current_website.company_id
            product = (
                self.env["product.product"].browse(combination_info["product_id"])
                or self
            )

            tax_display = (
                self.user_has_groups("account.group_show_line_subtotals_tax_excluded")
                and "total_excluded"
                or "total_included"
            )
            fpos = (
                self.env["account.fiscal.position"]
                .sudo()
                .get_fiscal_position(partner.id)
            )
            taxes = fpos.map_tax(
                product.sudo().taxes_id.filtered(lambda x: x.company_id == company_id),
                product,
                partner,
            )

            # The list_price is always the price of one.
            quantity_1 = 1
            combination_info["price"] = self.env[
                "account.tax"
            ]._fix_tax_included_price_company(
                combination_info["price"], product.sudo().taxes_id, taxes, company_id
            )
            price = taxes.compute_all(
                combination_info["price"],
                product.currency_id,
                quantity_1,
                product,
                partner,
            )[tax_display]
            list_price = price
            combination_info["price_extra"] = self.env[
                "account.tax"
            ]._fix_tax_included_price_company(
                combination_info["price_extra"],
                product.sudo().taxes_id,
                taxes,
                company_id,
            )
            price_extra = taxes.compute_all(
                combination_info["price_extra"],
                product.currency_id,
                quantity_1,
                product,
                partner,
            )[tax_display]
            has_discounted_price = (
                product.currency_id.compare_amounts(list_price, price) == 1
            )

            combination_info.update(
                price=price,
                list_price=list_price,
                price_extra=price_extra,
                has_discounted_price=has_discounted_price,
            )
        return combination_info

    def _get_image_holder_catalog(self):
        """Returns the holder of the image to use as default representation.
        If the product template has an image it is the product template,
        otherwise if the product has variants it is the first variant

        :return: this product template or the first product variant
        :rtype: recordset of 'product.template' or recordset of 'product.product'
        """
        self.ensure_one()
        if self.image_128:
            return self
        variant = self.env["product.product"].browse(
            self._get_first_possible_variant_id()
        )
        # if the variant has no image anyway, spare some queries by using template
        return variant if variant.image_variant_128 else self
