# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api

class ConsignmentType(models.Model):
    _name = "consignment.type"
    _description = "Consignment Type"

    _inherit = [
        "mail.thread",
    ]

    name = fields.Char(
        string="Consignment Type",
        required=True,
    )

    code = fields.Char(
        string="Code",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    description = fields.Text(
        string="Description",
    )

    sequence_id = fields.Many2one(
            string="Sequence",
            comodel_name="ir.sequence",
            company_dependent=True,
    )
