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

    consignment_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Consignment",
        comodel_name="res.groups",
        relation="rel_consignment_type_confirm",
        column1="type_id",
        column2="group_id",
    )

    consignment_approve_grp_ids = fields.Many2many(
        string="Allow To Approve Consignment",
        comodel_name="res.groups",
        relation="rel_consignment_type_approve",
        column1="type_id",
        column2="group_id",
    )

    consignment_open_grp_ids = fields.Many2many(
        string="Allow To Open Consignment",
        comodel_name="res.groups",
        relation="rel_consignment_type_open",
        column1="type_id",
        column2="group_id",
    )

    consignment_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Consignment",
        comodel_name="res.groups",
        relation="rel_consignment_type_cancel",
        column1="type_id",
        column2="group_id",
    )

    consignment_done_grp_ids = fields.Many2many(
        string="Allow To Finish Consignment",
        comodel_name="res.groups",
        relation="rel_consignment_type_done",
        column1="type_id",
        column2="group_id",
    )

    consignment_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Consignment",
        comodel_name="res.groups",
        relation="rel_consignment_type_restart",
        column1="type_id",
        column2="group_id",
    )
