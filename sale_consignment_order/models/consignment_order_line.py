# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ConsingnemtOrderLine(models.Model):
    _name = "consignment.order_line"
    _description = "Consignment Order Line"

    # membuat fungsi untuk field compute -->
    # depend berisi field yang akan digunakan dalam compute
    # tax_ids.amount tidak diikutsertakan karna jika dimasukkan akan berefek
    # jika terjadi perubahan amount dari tax id akan mempengaruhi nilai
    # pada consignment order line pada data yang sdh disimpan
    # document adalah identifikasi untuk current record
    # line adalah identifikasi untuk child dr current record
    @api.multi
    @api.depends(
        "price_unit",
        "quantity",
        "tax_ids",
    )
    def _compute_amount(self):
        for document in self:
            document.price_subtotal = document.price_unit * document.quantity
            tax_subtotal = 0.0
            for line in document.tax_ids:
                tax_subtotal += document.price_subtotal * line.amount
            document.tax_subtotal = tax_subtotal

    # @api.multi
    @api.depends(
        "order_id",
    )
    def _compute_date(self):
        for document in self:
            document.date = document.order_id.date_order

    # @api.multi
    @api.depends(
        "product_id",
    )
    def _compute_allowed_uom_ids(self):
        obj_uom = self.env["product.uom"]
        for document in self:
            result = []
            if document.product_id:
                criteria = [
                    ("category_id", "=", document.product_id.uom_id.category_id.id),
                ]
                result = obj_uom.search(criteria).ids
            document.allowed_uom_ids = result

    order_id = fields.Many2one(
        string="Consignment Order",
        comodel_name="consignment.order",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        domain=[("sale_ok", "=", True)],
        required=True,
        change_default=True,
        ondelete="restrict",
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
    )
    quantity = fields.Float(
        string="Quantity",
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    tax_ids = fields.Many2many(
        string="Tax",
        comodel_name="account.tax",
        relation="rel_consignment_order_line_2_account_tax",
        column1="order_line_id",
        column2="tax_ids",
    )
    tax_subtotal = fields.Float(
        string="Tax Total",
        compute="_compute_amount",
        store=True,
    )
    price_subtotal = fields.Float(
        string="Price Sub Total",
        compute="_compute_amount",
        store=True,
    )
    pricelist_id = fields.Many2one(
        string="Price List",
        comodel_name="product.pricelist",
        required=True,
    )
    date = fields.Date(
        string="Date",
        compute="_compute_date",
        store=False,
    )
    allowed_uom_ids = fields.Many2many(
        string="Allowed UoM",
        comodel_name="product.uom",
        compute="_compute_allowed_uom_ids",
        store=False,
    )

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id and self.product_id.uom_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "pricelist_id",
        "product_id",
        "quantity",
        "date",
        "uom_id",
    )
    def onchange_price_unit(self):
        price_unit = 0.0
        obj_uom = self.env["product.uom"]
        qty = 0.0

        ctx = {}
        if self.date:
            ctx.update({"date": self.date})

        if self.uom_id:
            qty = obj_uom._compute_qty_obj(
                from_unit=self.uom_id,
                qty=self.quantity,
                to_unit=self.product_id.uom_id,
            )

        if self.product_id and self.pricelist_id:
            price_unit = self.pricelist_id.with_context(ctx).price_get(
                prod_id=self.product_id.id,
                qty=qty,
            )[self.pricelist_id.id]

        if self.uom_id:
            price_unit = obj_uom._compute_price(
                from_uom_id=self.product_id.uom_id.id,
                price=price_unit,
                to_uom_id=self.uom_id.id,
            )

        self.price_unit = price_unit
