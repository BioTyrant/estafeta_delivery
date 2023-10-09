# -*- coding: utf-8 -*-
from odoo import models, fields, api


import requests


class estafeta_token(models.Model):
    _name = 'estafeta.token'
    _description = 'Estafeta Token store'

    name = fields.Char(string="Name", required="True")

    
    @api.model
    def _get_token(self):

        keys = self.env['access.key'].search([])
        import pdb;pdb.set_trace()


        
        token_url = "access_token.ESTAFETA['token_url']"

        # Credenciales
        client_id = "access_token.ESTAFETA['client_id']"
        client_secret = "access_token.ESTAFETA['client_secret']"

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
            print("Token obtenido:", token)
        else:
            print("Error al obtener el token. Código de estado:", response.status_code)
        return token




