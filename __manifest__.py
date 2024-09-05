# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'School_management',
    'author': 'prashanth',
    'version': '17.0.0.0',
    'license': 'LGPL-3',

    'data': ['security/ir.model.access.csv',
             'security/school_security.xml',
             'wizard/student_complaint_view.xml',
            'views/student.xml',
             'views/teacher.xml',
             'views/parents.xml',
             'views/admission.xml',
             'views/sale.xml',
             'views/invoice.xml',
             'views/student_complaint.xml',
             ],

    'depends': ['mail',
                'sale',
                'account',
                ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
