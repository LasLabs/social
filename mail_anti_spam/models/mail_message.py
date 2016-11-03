# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
