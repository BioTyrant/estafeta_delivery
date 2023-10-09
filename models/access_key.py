# -*- coding: utf-8 -*-

from odoo import models,fields, api



class access_key(models.Model):
    _name = "access.key"
    _description = "access key"

    name = fields.Char (string="Access Key", required=True)
    key_data = fields.Char (string="key", required=True)
