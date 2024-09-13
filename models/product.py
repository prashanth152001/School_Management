from odoo import models, fields


class ProductUpgrade(models.Model):
    _inherit = 'product.template'

    # Brands for products
    brand_id = fields.Many2one(comodel_name='product.brand', string='Product Brand')