# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


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
                tax_subtotal += (document.price_subtotal * line.amount)
            document.tax_subtotal = tax_subtotal

    order_id = fields.Many2one(
        string="Consignment Order",
        comodel_name="consignment.order",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product',
        domain=[('sale_ok', '=', True)],
        change_default=True,
        ondelete='restrict',
    )
    price_unit = fields.Float(
        string='Unit Price',
        required=True,

    )
    quantity = fields.Float(
        string='Quantity',
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
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

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id and self.product_id.uom_id:
            self.uom_id = self.product_id.uom_id
