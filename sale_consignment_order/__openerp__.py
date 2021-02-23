# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Sale Consignment Order",
    "version": "8.0.0.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_account",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_print_policy",
        "base_terminate_reason",
    ],
    "data": [
        "menu.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_terminate_reason_configurator_data.xml",
        "data/product_pricelist_type_data.xml",
        "views/consignment_type_views.xml",
        "views/consignment_order_views.xml",
        "views/res_partner_views.xml",
    ],
}
