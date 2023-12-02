# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product App - website Integration",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "auto_install": True,
    "depends": [
        "ssi_product",
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/templates.xml",
        "views/product_template_views.xml",
    ],
    "demo": [],
}
