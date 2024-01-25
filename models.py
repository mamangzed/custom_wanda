# custom_sales/models.py

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    request_vendor = fields.Char('Request Vendor')
    no_kontrak = fields.Char('No Kontrak')
    with_po = fields.Boolean('With PO')
