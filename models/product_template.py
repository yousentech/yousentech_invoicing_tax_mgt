# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class xx_add_fields_in_product(models.Model):
    _inherit = 'product.template'

    tax_reqiured = fields.Boolean(string="خاضع للضريبة", default=True)


class xx_sale_order_tax_required(models.Model):
    _inherit = 'sale.order.line'

    l_tax_reqiured = fields.Boolean()

    @api.onchange('product_id')
    def check_tax_required(self):
        for rec in self:
            if rec.product_id:
                rec.l_tax_reqiured = rec.product_id.tax_reqiured

class xx_account_move_line_tax_required(models.Model):
    _inherit = 'account.move.line'

    l_tax_reqiured = fields.Boolean()

    @api.onchange('product_id')
    def check_tax_required(self):
        for rec in self:
            if rec.product_id:
                rec.l_tax_reqiured = rec.product_id.tax_reqiured

class xx_account_move_tax_required(models.Model):
    _inherit = 'account.move'

    @api.constrains('invoice_line_ids')
    def check_tax_required(self):
        for rec in self:

            if rec.type in ('out_invoice','out_refund'):
                for line in rec.invoice_line_ids:
                    if line.product_id:
                        if line.product_id.tax_reqiured and not line.tax_ids:
                            raise ValidationError(
                                 "تنبيه .. لا يمكن الاستمرار لوجود ضريبة للمنتج (%s) " % line.product_id.name)

    def post(self):
        self.check_tax_required()
        return super(xx_account_move_tax_required, self).post()