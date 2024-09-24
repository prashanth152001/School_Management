from odoo import models
import base64
import io
from odoo.tools.safe_eval import datetime
import re, html


class PurchaseOrderXlsx(models.AbstractModel):
    _name = 'report.school.report_purchase_order_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, orders):
        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center'})
        align_right = workbook.add_format({'align': 'right'})
        price_format = workbook.add_format({'num_format': '#,##0.00'})
        price_format_bold_bordered_except_left = workbook.add_format({'num_format': '#,##0.00', 'bold': True, 'right': 1, 'top': 1, 'bottom': 1, 'border_color': 'black'})
        price_format_bordered = workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'border_color': 'black'})
        price_format_bordered_except_left = workbook.add_format({'num_format': '#,##0.00', 'right': 1, 'top': 1, 'bottom': 1, 'border_color': 'black'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        date_format_centered = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center', 'border': 1, 'border_color': 'black'})
        date_format_bordered = workbook.add_format({'num_format': 'dd mmmm, yyyy', 'border': 1, 'border_color': 'black', 'align': 'left'})
        bordered = workbook.add_format({'border': 1, 'border_color': 'black'})
        border_except_right = workbook.add_format({'left': 1, 'top': 1, 'bottom': 1, 'border_color': 'black', 'align': 'right'})
        border_except_left = workbook.add_format({'right': 1, 'top': 1, 'bottom': 1, 'border_color': 'black'})
        bordered_centered = workbook.add_format({'border': 1, 'border_color': 'black', 'align': 'center'})
        format_1 = workbook.add_format({'bold': True, 'bg_color': '#1d66b8', 'color': 'white'})
        format_2 = workbook.add_format({'bold': True, 'bg_color': '#1d66b8', 'align': 'center', 'color': 'white', 'border': 1, 'border_color': 'black'})
        format_3 = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20})
        format_4 = workbook.add_format({'align': 'center', 'bottom': 4, 'bottom_color': 'blue'})
        bold_bordered = workbook.add_format({'bold': True, 'border': 1, 'border_color': 'black'})
        format_6 = workbook.add_format({'align': 'center', 'bold': True, 'color': '#120d51', 'font_size': 20})
        bold_bordered_except_right = workbook.add_format({'bold': True, 'align': 'right', 'left': 1, 'top': 1, 'bottom': 1, 'border_color': 'black'})
        format_7 = workbook.add_format({'text_wrap': True, 'border': 1, 'border_color': 'black'})

        # Function to remove HTML tags
        def remove_html_tags(text):
            clean = re.sub('<.*?>', '', text)  # Regex to remove HTML tags
            clean= html.unescape(clean)
            clean = re.sub('[.]', '. ', clean)
            return clean

        for obj in orders:
            report_name = obj.name
            sheet = workbook.add_worksheet(report_name[:31])
            sheet.hide_gridlines(2)
            sheet.set_column('K:K', 5)
            sheet.set_column('L:L', 15)
            sheet.set_column('J:J', 10)
            sheet.set_row(22, 40)

            #Left align elements
            row = 0
            col = 0

            if obj.company_id.logo:
                company_logo = io.BytesIO(base64.b64decode(obj.company_id.logo))
                sheet.insert_image(row, col, "logo.png", {'image_data': company_logo, 'x_scale': 0.5, 'y_scale': 0.5})
                row += 3

            row = 0
            col = 8
            quotation_state = ['draft', 'sent', 'to approve']
            order_state = ['purchase', 'done']
            cancel_state = ['cancel']
            if obj.state in quotation_state:
                sheet.merge_range(row, col, row + 1, col + 3, "Request for Quotation", format_6)
            elif obj.state in order_state:
                sheet.merge_range(row, col, row + 1, col + 3, "Purchase Order", format_6)
            elif obj.state in cancel_state:
                sheet.merge_range(row, col, row + 1, col + 3, "Cancelled Order", format_6)

            row += 4
            col = 0
            address_line1 = obj.company_id.street or ""
            if obj.company_id.street2:
                address_line1 += " " + obj.company_id.street2
            address_line2 = obj.company_id.city or ""
            if obj.company_id.state_id:
                address_line2 += " " + obj.company_id.state_id.name
            address_line3 = obj.company_id.country_id.name or ""
            if obj.company_id.country_code:
                address_line3 += " " + obj.company_id.country_code
            if obj.company_id.zip:
                address_line3 += " " + obj.company_id.zip
            sheet.merge_range(row, col, row, col + 3, address_line1)
            col = 8
            sheet.merge_range(row, col, row, col + 1, "Date:", bordered)
            col += 2
            sheet.merge_range(row, col, row, col + 1, datetime.datetime.today(), date_format_bordered)
            col = 0
            row += 1
            sheet.merge_range(row, col, row, col + 3, address_line2)
            col = 8
            sheet.merge_range(row, col, row, col + 1, "Order #:", bordered)
            col += 2
            sheet.merge_range(row, col, row, col + 1, obj.name, bordered)
            col = 0
            row += 1
            sheet.merge_range(row, col, row, col + 3, address_line3)
            col = 8
            if obj.state in quotation_state:
                sheet.merge_range(row, col, row, col + 1, "Valid Until:", bordered)
                col += 2
                sheet.merge_range(row, col, row, col + 1, obj.date_order, date_format_bordered)
            else:
                sheet.merge_range(row, col, row, col + 1, "Order Date:", bordered)
                col += 2
                sheet.merge_range(row, col, row, col + 1, obj.date_approve, date_format_bordered)

            row += 3
            col = 0
            sheet.merge_range(row, col, row, col + 3, "Invoicing Address:", format_1)
            col = 8
            sheet.merge_range(row, col, row, col + 3, "Shipping Address:", format_1)
            col = 0
            if obj.partner_id.name:
                row += 1
                sheet.merge_range(row, col,row, col + 3, obj.partner_id.name)
                col = 8
                sheet.merge_range(row, col, row, col + 3, obj.partner_id.name)
            row += 1
            col = 0
            inv_address_line1 = obj.partner_id.street or ""
            if obj.partner_id.street2:
                inv_address_line1 += " " + obj.partner_id.street2
            inv_address_line2 = obj.partner_id.city or ""
            if obj.partner_id.state_id:
                inv_address_line2 += " " + obj.partner_id.state_id.name
            inv_address_line3 = obj.partner_id.country_id.name or ""
            if obj.partner_id.country_code:
                inv_address_line3 += " " + obj.partner_id.country_code
            if obj.partner_id.zip:
                inv_address_line3 += " " + obj.partner_id.zip
            sheet.merge_range(row, col, row, col + 3, inv_address_line1)
            col = 8
            sheet.merge_range(row, col, row, col + 3, inv_address_line1)
            row += 1
            col = 0
            sheet.merge_range(row, col, row, col + 3, inv_address_line2)
            col = 8
            sheet.merge_range(row, col, row, col + 3, inv_address_line2)
            row += 1
            col = 0
            sheet.merge_range(row, col, row, col + 3, inv_address_line3)
            col = 8
            sheet.merge_range(row, col, row, col + 3, inv_address_line3)

            row += 4
            col = 0
            sheet.merge_range(row, col, row, col + 1, "Buyer", format_2)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "Shipping Method", format_2)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "Shipping Terms", format_2)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "Payment Terms", format_2)
            col += 2
            if obj.state in order_state:
                sheet.merge_range(row, col, row, col + 1, "Confirmation Date", format_2)
            else:
                sheet.merge_range(row, col, row, col + 1, "Order Deadline", format_2)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "Expected Arrival", format_2)
            row += 1
            col = 0
            sheet.merge_range(row, col, row, col + 1, obj.user_id.name, bordered_centered)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "", bordered_centered)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "", bordered_centered)
            col += 2
            sheet.merge_range(row, col, row, col + 1, obj.payment_term_id.name, bordered_centered)
            col += 2
            sheet.merge_range(row, col, row, col + 1, obj.date_order, date_format_centered)
            col += 2
            sheet.merge_range(row, col, row, col + 1, obj.date_planned, date_format_centered)

            row += 3
            col = 0
            sheet.merge_range(row, col, row, col + 1, "Product", format_2)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "Description", format_2)
            col += 2
            sheet.merge_range(row, col, row, col + 1, "Expected Arrival", format_2)
            col += 2
            sheet.write(row, col, "Qty", format_2)
            col += 1
            sheet.merge_range(row, col, row, col + 1, "Unit Price", format_2)
            col += 2
            sheet.write(row, col, "Taxes", format_2)
            col += 1
            sheet.merge_range(row, col, row, col + 1, "Total", format_2)
            row += 1
            product_values = obj.order_line
            for product in product_values:
                col = 0
                sheet.merge_range(row, col, row, col + 1, product.product_id.name, bordered)
                col += 2
                products_list = product.name.split('\n')
                product_names = ""
                if len(products_list) > 1:
                    for name in products_list:
                        product_names += "\n" + "* " + name
                else:
                    product_names = products_list[0]
                sheet.merge_range(row, col, row, col + 1, product_names, bordered)
                col += 2
                sheet.merge_range(row, col, row, col + 1, product.date_planned, date_format_centered)
                col += 2
                sheet.write(row, col, product.product_qty, bordered_centered)
                col += 1
                sheet.merge_range(row, col, row, col + 1, product.price_unit, price_format_bordered)
                col += 2
                taxes = ""
                for tax in product.taxes_id:
                    taxes += '\n' + tax.name
                sheet.write(row, col, taxes, bordered_centered)
                col += 1
                sheet.merge_range(row, col, row, col + 1, product.price_total, price_format_bordered)
                row += 1

            col = 0
            row += 1
            sheet.merge_range(row, col, row, col + 7, "Special Notes and Instructions", format_2)
            col += 9
            sheet.write(row, col, "Subtotal", bordered)
            col += 1
            sheet.write(row, col, obj.currency_id.symbol, border_except_right)
            col += 1
            sheet.write(row, col, obj.amount_untaxed, price_format_bordered_except_left)
            row += 1
            col = 0
            html_notes = obj.notes
            text_notes = remove_html_tags(html_notes)
            sheet.merge_range(row, col, row + 1, col + 7, text_notes, format_7)
            col = 9
            sheet.write(row, col, "Taxes", bordered)
            col += 1
            sheet.write(row, col, obj.currency_id.symbol, border_except_right)
            col += 1
            sheet.write(row, col, obj.amount_tax, price_format_bordered_except_left)
            row += 1
            col = 9
            sheet.write(row, col, "Total", bold_bordered)
            col += 1
            sheet.write(row, col, obj.currency_id.symbol, bold_bordered_except_right)
            col += 1
            sheet.write(row, col, obj.amount_total, price_format_bold_bordered_except_left)

            row += 4
            col = 0
            sheet.merge_range(row, col, row + 1, col + 11, "Thank you for your business!", format_3)
            row += 2
            sheet.merge_range(row, col, row, col + 11, "Should you have any enquiries concerning this quotation, please contact " + obj.user_id.name + " on " + str(obj.user_id.phone), format_4)
            row += 1
            sheet.merge_range(row, col, row, col + 11, f"{obj.company_id.street}, {obj.company_id.street2}, {obj.company_id.city}, {obj.company_id.state_id.name}, {obj.company_id.country_id.name}, {obj.company_id.country_code}, {obj.company_id.zip}", center)
            row += 1
            sheet.merge_range(row, col, row, col + 11, f"Phone: {obj.company_id.phone}  Email: {obj.company_id.email}  Website: {obj.company_id.website}", center)
