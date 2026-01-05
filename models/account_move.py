# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

 

class xx_account_move_tax_required(models.Model):
    _inherit = 'account.move'

    # *******************************************************************************************************
    allow_modify_product_tax_in_invoice = fields.Boolean(
        default=lambda self: self._default_allow_modify_product_tax_in_invoice(),
        compute="_get_allow_modify_product_tax_in_invoice")

    # @api.depends('company_id')
    def _get_allow_modify_product_tax_in_invoice(self):
        for rec in self:
            rec.allow_modify_product_tax_in_invoice = self.user_has_groups(
                'yousentech_invoicing_tax_mgt.group_allow_modify_product_tax_in_invoice')

    def _default_allow_modify_product_tax_in_invoice(self):
        return self.user_has_groups('yousentech_invoicing_tax_mgt.group_allow_modify_product_tax_in_invoice')
    # *******************************************************************************************************