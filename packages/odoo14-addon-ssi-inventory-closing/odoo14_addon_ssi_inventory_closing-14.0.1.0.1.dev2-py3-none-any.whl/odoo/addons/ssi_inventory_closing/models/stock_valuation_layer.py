# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class StockValuationLayer(models.Model):
    _name = "stock.valuation.layer"
    _inherit = [
        "stock.valuation.layer",
    ]

    inventory_closing_id = fields.Many2one(
        string="# Inventory Closing",
        comodel_name="inventory_closing",
        ondelete="set null",
    )
