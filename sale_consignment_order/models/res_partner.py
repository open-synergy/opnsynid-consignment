# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    default_sale_consignment_pricelist_id = fields.Many2one(
        string="Default Sale Consignment Pricelist",
        comodel_name="product.pricelist",
        company_dependent=True,
    )

    
