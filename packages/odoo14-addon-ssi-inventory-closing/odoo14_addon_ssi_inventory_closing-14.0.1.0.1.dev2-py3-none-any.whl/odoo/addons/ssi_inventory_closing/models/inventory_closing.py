# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class InventoryClosing(models.Model):
    _name = "inventory_closing"
    _description = "Inventory Closing"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_terminate",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        comodel_name="inventory_closing_type",
        string="Type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    stock_valuation_layer_ids = fields.One2many(
        string="Stock Valuation Layers",
        comodel_name="stock.valuation.layer",
        inverse_name="inventory_closing_id",
    )
    stock_move_ids = fields.One2many(
        string="Stock Moves",
        comodel_name="stock.move",
        inverse_name="inventory_closing_id",
    )
    account_move_ids = fields.Many2many(
        string="Accounting Entries",
        comodel_name="account.move",
        compute="_compute_account_move_ids",
        store=False,
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_product_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Allowed Product Category",
        compute="_compute_allowed_product_category_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_picking_type_ids = fields.Many2many(
        comodel_name="stock.picking.type",
        string="Allowed Picking Types",
        compute="_compute_allowed_picking_type_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_picking_type_category_ids = fields.Many2many(
        comodel_name="picking_type_category",
        string="Allowed Picking Type Categories",
        compute="_compute_allowed_picking_type_category_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "stock_valuation_layer_ids",
        "stock_valuation_layer_ids.debit_move_line_id",
        "stock_valuation_layer_ids.credit_move_line_id",
    )
    def _compute_account_move_ids(self):
        for record in self:
            record.account_move_ids = self.stock_valuation_layer_ids.mapped(
                "account_move_id"
            )

    @api.depends("type_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.type_id.product_selection_method,
                    manual_recordset=record.type_id.product_ids,
                    domain=record.type_id.product_domain,
                    python_code=record.type_id.product_python_code,
                )
            record.allowed_product_ids = result

    @api.depends("type_id")
    def _compute_allowed_product_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.category",
                    method_selection=record.type_id.product_category_selection_method,
                    manual_recordset=record.type_id.product_category_ids,
                    domain=record.type_id.product_category_domain,
                    python_code=record.type_id.product_category_python_code,
                )
            record.allowed_product_category_ids = result

    @api.depends("type_id")
    def _compute_allowed_picking_type_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="stock.picking.type",
                    method_selection=record.type_id.picking_type_selection_method,
                    manual_recordset=record.type_id.picking_type_ids,
                    domain=record.type_id.picking_type_domain,
                    python_code=record.type_id.picking_type_python_code,
                )
            record.allowed_picking_type_ids = result

    @api.depends("type_id")
    def _compute_allowed_picking_type_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="picking_type_category",
                    method_selection=record.type_id.picking_type_category_selection_method,
                    manual_recordset=record.type_id.picking_type_category_ids,
                    domain=record.type_id.picking_type_category_domain,
                    python_code=record.type_id.picking_type_category_python_code,
                )
            record.allowed_picking_type_category_ids = result

    def action_reload_stock_move(self):
        for record in self.sudo():
            record._reload_stock_move()

    def _reload_stock_move(self):
        self.ensure_one()
        StockMove = self.env["stock.move"]
        self.stock_move_ids.write(
            {
                "inventory_closing_id": False,
            }
        )
        stock_moves = StockMove.search(self._prepare_stock_move_domain())
        self.stock_valuation_layer_ids.write(
            {
                "inventory_closing_id": False,
            }
        )
        stock_valuation_layers = stock_moves.mapped(
            "stock_valuation_layer_ids"
        ).filtered(
            lambda r: r.debit_account_id
            and r.credit_account_id
            and not r.debit_move_line_id
            and not r.credit_move_line_id
            and not r.inventory_closing_id
        )
        stock_valuation_layers.write(
            {
                "inventory_closing_id": self.id,
            }
        )
        stock_valuation_layers.mapped("stock_move_id").write(
            {
                "inventory_closing_id": self.id,
            }
        )

    def _prepare_stock_move_domain(self):
        self.ensure_one()
        date_start = fields.Datetime.to_datetime(self.date_start)
        date_end = fields.Datetime.to_datetime(self.date_end)
        return [
            "&",
            "&",
            "&",
            "&",
            "&",
            ("state", "=", "done"),
            ("date", ">=", date_start),
            ("date", "<=", date_end),
            ("account_move_ids", "=", False),
            "|",
            ("product_id", "in", self.allowed_product_ids.ids),
            ("product_id.categ_id", "child_of", self.allowed_product_category_ids.ids),
            "|",
            ("picking_type_id", "in", self.allowed_picking_type_ids.ids),
            (
                "picking_type_id.category_id",
                "in",
                self.allowed_picking_type_category_ids.ids,
            ),
        ]

    @api.model
    def _get_policy_field(self):
        res = super(InventoryClosing, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "cancel_ok",
            "done_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.post_done_action()
    def _01_create_aml_from_svl(self):
        self.ensure_one()
        for svl in self.stock_valuation_layer_ids:
            svl._create_accounting_entry()

    @ssi_decorator.post_cancel_action()
    def _01_delete_aml(self):
        self.ensure_one()
        for svl in self.stock_valuation_layer_ids:
            svl._delete_accounting_entry()

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
