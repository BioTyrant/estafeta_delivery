# -*- coding: utf-8 -*-
from odoo import models, fields, api


import requests


class estafeta_token(models.Model):
    _name = 'estafeta.token'
    _description = 'Estafeta Token store'

    name = fields.Char(string="Name", required="True")


    def _get_keys(self,key_name):      

        key_id = self.env['access.key'].search([('name','=',key_name)])
        key = ''
        for k in key_id:
            key = k['key_data']
        return key
    
    @api.model
    def _get_token(self):
        
        token_url = self._get_keys('token_url')
        client_id = self._get_keys('client_id')
        client_secret = self._get_keys('client_secret')


        
        token_url = token_url

        # Credenciales
        client_id = client_id
        client_secret = client_secret

        # Parámetros de la solicitud
        payload = {
            "grant_type": "client_credentials",
            "scope": "execute"
        }

        # Autenticación
        auth = (client_id, client_secret)

        # Realizar la solicitud
        response = requests.post(token_url, data=payload, auth=auth)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            # Token obtenido
            token = response.json()["access_token"]
            # print("Token obtenido:", token)
        else:
            print("Error al obtener el token. Código de estado:", response.status_code)
        return token

    
    def _insert_token(self):
        print('Insertando Token en Base' + ' ' + self._get_token())
        vals = {
            'name' : self._get_token()
        }

        new_record = self.create(vals)
        

