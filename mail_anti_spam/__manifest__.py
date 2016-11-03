# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{

    'name': 'Mail Anti-Spam',
    'summary': 'It provides spam protection for Odoo messages on an opt-in'
               'basis.',
    'version': '10.0.1.0.0',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'category': 'Discussions',
    'external_dependencies': {
        'python' : [
            'numpy',
            'pandas',
            'sklearn',
            'textblob',
        ]
    },
    'website': 'https://laslabs.com',
    'license': 'LGPL-3',
    'installable': True,
}
