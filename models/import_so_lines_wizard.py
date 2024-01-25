# custom_nama/models/import_so_lines_wizard.py

from odoo import api, models, fields
import base64
from io import BytesIO
import xlsxwriter

class ImportSOLinesWizard(models.TransientModel):
    _name = 'import.so.lines.wizard'
    _description = 'Import Sales Order Lines Wizard'

    @api.multi
    def action_download_template(self):
        workbook = xlsxwriter.Workbook('/tmp/so_lines_template.xlsx')
        worksheet = workbook.add_worksheet()

        header_format = workbook.add_format({'bold': True})
        worksheet.write('A1', 'Product Code', header_format)
        worksheet.write('B1', 'Quantity', header_format)
        worksheet.write('C1', 'Unit Price', header_format)

        output = BytesIO()
        workbook.close()
        output.seek(0)

        file_data = output.read()
        file_data_base64 = base64.b64encode(file_data)
        self.write({'file': file_data_base64, 'file_name': 'so_lines_template.xlsx'})

        return {
            'name': 'Download Template',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=import.so.lines.wizard&id=%s&field=file&filename_field=file_name&download=true&filename=so_lines_template.xlsx' % (self.id),
            'target': 'self',
        }

    @api.multi
    def action_import_so_lines(self):
        file_content = base64.b64decode(self.file)

        workbook = xlrd.open_workbook(file_contents=file_content)
        worksheet = workbook.sheet_by_index(0)

        num_rows = worksheet.nrows - 1

        for row_index in range(1, num_rows + 1):
            product_code = worksheet.cell_value(row_index, 0)
            quantity = worksheet.cell_value(row_index, 1)
            unit_price = worksheet.cell_value(row_index, 2)


            self.env['sale.order.line'].create({
                'order_id': order_id,  # Sesuaikan dengan ID Sales Order yang sesuai
                'product_id': product_id,  # Sesuaikan dengan ID Produk yang sesuai
                'product_uom_qty': quantity,
                'price_unit': unit_price,
            })

        return {'type': 'ir.actions.act_window_close'}
