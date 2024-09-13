from odoo import fields, models


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'
    _rec_name = 'brand_name'

    brand_name = fields.Char(string='Product Brand', required=True)
