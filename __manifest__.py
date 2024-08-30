# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'School_management',
    'author': 'prashanth',

    'data': ['security/ir.model.access.csv',
            'views/student.xml',
             'views/teacher.xml',
             ],
    'depends': ['mail',],
    'installable': True,
    'application': True,
}
