# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'School_management',
    'author': 'prashanth',
    'version': '17.0.0.0',
    'license': 'LGPL-3',

    'data': ['security/ir.model.access.csv',
            'views/student.xml',
             'views/teacher.xml',
             'views/parents.xml',
             'views/admission.xml',
             'views/sale.xml',
             ],

    'depends': ['mail',
                'sale',
                ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
