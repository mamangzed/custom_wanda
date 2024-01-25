# custom_sales/models/custom_sales.py

from odoo import api, models, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    request_vendor = fields.Char('Request Vendor')
    no_kontrak = fields.Char('No Kontrak')
    with_po = fields.Boolean('With PO')
    purchase_orders = fields.One2many('purchase.order', 'sale_order_id', 'Purchase Orders')

    @api.multi
    def action_create_po(self):
        for order in self:
            if not order.with_po:
                raise UserError(_("Cannot create PO for this order."))

            po_vals = {
                'partner_id': order.request_vendor.id,
                'origin': order.name,
                'order_id': order.id,
            }
            po = self.env['purchase.order'].create(po_vals)

            for line in order.order_line:
                po_line_vals = {
                    'order_id': po.id,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'date_planned': line.confirmation_date or fields.Datetime.now(),
                }
                self.env['purchase.order.line'].create(po_line_vals)

            order.write({'state': 'purchase'})
        return True

    @api.multi
    def action_open_import_so_lines_wizard(self):
        return {
            'name': 'Import Sales Order Lines',
            'view_mode': 'form',
            'view_id': self.env.ref('custom_sales.view_import_so_lines_wizard_form').id,
            'view_type': 'form',
            'res_model': 'sale.order.import.lines.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.no_kontrak:
                existing_order = self.search([('no_kontrak', '=', order.no_kontrak), ('state', '=', 'sale')])
                if existing_order and existing_order != order:
                    raise UserError(_("No Kontrak sudah pernah diinputkan sebelumnya...!"))
            super(SaleOrder, order).action_confirm()
        return True
