# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ConsignmentOrder(models.Model):
    _name = "consignment.order"
    _description = "Consignment Order"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]

    # membuat nilai default untuk yang bersifat tdk konstan
    @api.model
    def _default_date_order(self):
        return fields.Datetime.now()

    # membuat fungsi untuk field compute -->
    # depend berisi field yang akan digunakan dalam compute
    @api.multi
    @api.depends(
        "detail_ids",
        "detail_ids.price_subtotal",
        "detail_ids.tax_subtotal",
    )
    def _compute_amount_total(self):
        for document in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for line in document.detail_ids:
                amount_untaxed += line.price_subtotal
                amount_tax += line.tax_subtotal
                amount_total += amount_untaxed + amount_tax
            document.amount_total = amount_total
            document.amount_tax = amount_tax
            document.amount_untaxed = amount_untaxed

    @api.multi
    def _compute_policy(self):
        _super = super(ConsignmentOrder, self)
        _super._compute_policy()

    name = fields.Char(
        string="Consignmet Order",
        required=True,
        default="/",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        ondelete="restrict", # pilihan: resttrict, cascade, set null
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_order = fields.Datetime(
        string="Order Date",
        required=True,
        readonly=True,
        default=lambda self: self._default_date_order(),
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Consignment Type",
        comodel_name="consignment.type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pricelist_id = fields.Many2one(
        string="Price List",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Pricelist for current consignment order.",
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    note = fields.Text(
        string="Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirm", "Waiting For Approval"),
        ("approve", "Ready to Process"),
        ("open", "In Progress"),
        ("cancel", "Cancelled"),
        ("done", "Done"),
        ("terminate", "Terminated"),
    ],
        string="Status",
        default="draft",
    )

    amount_untaxed = fields.Float(
        string="Amount Untaxed",
        store=True,
        compute="_compute_amount_total"
    )

    amount_tax = fields.Float(
        string="Amount Taxed",
        store=True,
        compute="_compute_amount_total"
    )

    amount_total = fields.Float(
        string="Amount Total",
        store=True,
        compute="_compute_amount_total"
    )

    detail_ids = fields.One2many(
        string="Order Line",
        comodel_name="consignment.order_line",
        inverse_name="order_id",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    # Policy Fields
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy"
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy"
    )
    open_ok = fields.Boolean(
        string="Can Open",
        compute="_compute_policy"
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy"
    )
    done_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy"
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy"
    )
    terminate_ok = fields.Boolean(
        string="Can Terminate",
        compute="_compute_policy"
    )

    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
    )
    approve_date = fields.Datetime(
        string="Approve Date",
        readonly=True,
    )
    approve_user_id = fields.Many2one(
        string="Approve By",
        comodel_name="res.users",
        readonly=True,
    )
    open_user_id = fields.Many2one(
        string="Opened By",
        comodel_name="res.users",
        readonly=True,
    )
    open_date = fields.Datetime(
        string="Open Date",
        readonly=True,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
    )
    restart_date = fields.Datetime(
        string="Restart Date",
        readonly=True,
    )
    restart_user_id = fields.Many2one(
        string="Restart By",
        comodel_name="res.users",
        readonly=True,
    )
    terminate_date = fields.Datetime(
        string="Terminate Date",
        readonly=True,
    )
    terminate_user_id = fields.Many2one(
        string="Terminate By",
        comodel_name="res.users",
        readonly=True,
    )

    # merubah pricelist_id berdasarkan partner
    @api.onchange(
        "partner_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False
        if self.partner_id and self.partner_id.default_sale_consignment_pricelist_id:
            self.pricelist_id = self.partner_id.default_sale_consignment_pricelist_id

    # fungsi saat menekan tombol confirm dilakukan
    # perubahan data state user dan tanggal dengan menjalankan fungsi
    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())

    # fungsi saat menekan tombol terminate dilakukan
    # perubahan data state user dan tanggal dengan menjalankan fungsi
    @api.multi
    def action_terminate(self):
        for document in self:
            document.write(document._prepare_terminate_data())

    # fungsi saat menekan tombol approve dilakukan
    # perubahan data state user dan tanggal dengan menuliskan statement langsung
    @api.multi
    def action_approve(self):
        for document in self:
            document.write(document._prepare_approve_data())

    @api.multi
    def action_open(self):
        for document in self:
            document.write(document._prepare_open_data())

    @api.multi
    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    # fungsi perubahan data state user dan tanggal -- approve
    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        result = {
            "state": "approve",
            "approve_date": fields.Datetime.now(),
            "approve_user_id": self.env.user.id,
        }
        return result

    # fungsi perubahan data state user dan tanggal -- open
    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        result = {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }
        return result

    # fungsi perubahan data state user dan tanggal -- done
    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        result = {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }
        return result

    # fungsi perubahan data state user dan tanggal -- done
    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        result = {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }
        return result

    # fungsi perubahan data state user dan tanggal -- restart
    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
            "restart_date": fields.Datetime.now(),
            "restart_user_id": self.env.user.id,
            "confirm_date": False,
            "confirm_user_id": False,
            "approve_date": False,
            "approve_user_id": False,
            "open_date": False,
            "open_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }
        return result

    # fungsi perubahan data state user dan tanggal -- confirm
    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }
        return result

    # fungsi perubahan data state user dan tanggal -- terminate
    @api.multi
    def _prepare_terminate_data(self):
        self.ensure_one()
        result = {
            "state": "terminate",
            "terminate_date": fields.Datetime.now(),
            "terminate_user_id": self.env.user.id,
        }
        return result

    # constraint berfungsi sebagai validasi terhadap object / field
    @api.constrains(
        "name",
        "state",
    )
    # mengeceak konsistensi antara object name dan state
    def _check_document_number(self):
        for document in self:
            if document.name == "/" and document.state != "draft":
                raise UserError("Error")

    @api.model
    def create(self, values):
        _super = super(ConsignmentOrder, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write({
            "name": sequence,
        })
        return result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(ConsignmentOrder, self)
        _super.unlink()
