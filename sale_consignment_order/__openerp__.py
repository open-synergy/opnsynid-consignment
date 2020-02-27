# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Sale Consignment Order",
    "version": "8.0.1.0.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_account",
        "base_sequence_configurator",
    ],
    "data": [
        "menu.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "views/consignment_type_views.xml",
        "views/consignment_order_views.xml",
        "views/res_partner_views.xml",
    ],
}
