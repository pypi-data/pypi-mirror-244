# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move"]

    inventory_closing_id = fields.Many2one(
        string="# Inventory Closing",
        comodel_name="inventory_closing",
        ondelete="set null",
    )
