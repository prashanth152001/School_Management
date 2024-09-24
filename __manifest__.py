# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'School_management',
    'author': 'prashanth',
    'version': '17.0.0.0',
    'license': 'LGPL-3',

    'data': ['security/school_security.xml',
             'security/ir.model.access.csv',
             'data/mail_template_student.xml',
             'data/ir_cron_fee_due_mail.xml',
             'data/mail_template_fee_due_remainder.xml',
             'wizard/student_complaint_view.xml',
             'views/student.xml',
             'views/teacher.xml',
             'views/parents.xml',
             'views/admission.xml',
             'views/sale.xml',
             'views/invoice.xml',
             'views/product.xml',
             'views/purchase.xml',
             'views/student_complaint.xml',
             'report/fee_structure_template.xml',
             'report/fee_structure_report.xml',
             'report/sale_quotation_template.xml',
             'report/sale_quotation_report.xml',
             'report/invoice_report_inherit.xml',
             'report/purchase_order_template.xml',
             'report/purchase_order_report.xml',
             'report/purchase_order_report_xlsx.xml',
             ],

    'depends': ['mail',
                'sale',
                'account',
                'purchase',
                'report_xlsx',
                ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
