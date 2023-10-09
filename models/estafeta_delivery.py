# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests

class estafeta_delivery(models.TransientModel):
    _name = 'estafeta_delivery.wizard'
    _description = 'Guide generator'
    
    def _default_session(self):
        session_obj = self.env['account.move']
        session_id = self._context.get('active_id')
        session_record = session_obj.browse(session_id)
        # import pdb; pdb.set_trace()
        return session_record
    
    @api.depends('address')
    def _address_name(self):
        for record in self:
            try:
                if self.address:
                    self.address_name = self.address.split("|")[0].strip()
                    self.address_last_name = self.address.split("|")[1].strip()
                    self.address_street = self.address.split("|")[2].strip()
                    self.address_province = self.address.split("|")[3].strip()
                    self.address_city = self.address.split("|")[4].strip()
                    self.address_post_code = self.address.split("|")[5].strip()
                    self.address_country = self.address.split("|")[6].strip()                       
                    self.address_telephone = self.address.split("|")[7].strip()
            except Exception as e:
                print(f'unerror:{e}')
    
    def get_token(self):

        pass
    
    
    description = fields.Text()
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly="1", default = _default_session)
    shipping_type = fields.Char (string="Shipping type", related= "invoice_id.x_studio_tipo_de_envo")
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", related= "invoice_id.x_sale_order" )
    address = fields.Text(string="Address", related= "sale_order_id.x_studio_notas_para_cedis_1")
    address_name = fields.Char(string="Name",  compute=_address_name)
    address_last_name = fields.Char(string="Last Name", readonly="1")
    address_street = fields.Char(string="Street", readonly="1")
    address_province = fields.Char(string="Province", readonly="1")
    address_city = fields.Char(string="City", readonly="1")
    address_post_code = fields.Char(string="Post Code", readonly="1")
    address_country = fields.Char(string="Country", readonly="1")
    address_telephone = fields.Char(string="Telephone", readonly="1")

    







