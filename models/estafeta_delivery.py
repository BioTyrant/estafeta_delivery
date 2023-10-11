# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

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
    
    def _get_token(self):

        token_id = self.env['estafeta.token'].search([], order='id desc', limit=1)
        token = ''
        for tk in token_id:
            token =  tk['name']
        return token
    
    def _get_keys(self,key_name):      

        key_id = self.env['access.key'].search([('name','=',key_name)])
        key = ''
        for k in key_id:
            key = k['key_data']
        return key
        
        


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
    

    def _tracking_estafeta(self):
        token = self._get_token()


        if token:
            
            traking_url = self._get_keys('traking_url')
            apikey = self._get_keys('client_id')

            endpoint = traking_url

            headers = {
                'Authorization': f'Bearer {token}',  # Corregido aquí
                'apikey': apikey,
                'Content-Type': 'application/json'  # Corregido aquí
            }

            data = {
                "identification": {
                    "suscriberId": "HZ",
                    "customerNumber": "8545726"
                },
                "systemInformation": {
                    "id": "AP01",
                    "name": "AP01",
                    "version": "1.10.20"
                },
                "labelDefinition": {
                    "wayBillDocument": {
                        "aditionalInfo": "string",
                        "content": "Documents",
                        "costCenter": "SPMXA12345",
                        "customerShipmentId": "",
                        "referenceNumber": "Ref1",
                        "groupShipmentId": ""
                    },
                    "itemDescription": {
                        "parcelId": 4,
                        "weight": 10.5,
                        "height": 20,
                        "length": 30,
                        "width": 10
                    },
                    "serviceConfiguration": {
                        "quantityOfLabels": 5,
                        "serviceTypeId": "70",
                        "salesOrganization": "502",
                        "originZipCodeForRouting": "06170",
                        "isInsurance": False,
                        "isReturnDocument": False
                    },
                    "location": {
                        "isDRAAlternative": False,
                        "origin": {
                            "contact": {
                                "corporateName": "Grupo Comrap SA de CV",
                                "contactName": "Alejandro Oseguera",
                                "telephone": "5583027126",
                                "email": "alejandrooseguera@mitzu.com"
                            },
                            "address": {
                                "bUsedCode": True,
                                "roadTypeCode": "001",
                                "roadTypeAbbName": "string",
                                "roadName": "Calle San Juan",
                                "townshipCode": "07460",
                                "townshipName": "Gustavo A Madero",
                                "settlementTypeCode": "001",
                                "settlementTypeAbbName": "string",
                                "settlementName": "Col Granjas Modernas",
                                "stateCode": "09",
                                "stateAbbName": "Ciudad México",
                                "zipCode": "07460",
                                "countryCode": "484",
                                "countryName": "MEX",
                                "externalNum": "763",
                                "localityName": "Gustavo A Madero"
                            }
                        },
                        "destination": {
                            "isDeliveryToPUDO": False,
                            "deliveryPUDOCode": "567",
                            "homeAddress": {
                                "contact": {
                                    "corporateName": self.address_name + " " + self.address_last_name[:29],
                                    "contactName": self.address_name + " " + self.address_last_name[:29],
                                    "telephone": self.address_telephone,
                                    # "email": "manfredjuarez100@gmail.com"
                                },
                                "address": {
                                    "bUsedCode": True,
                                    "roadTypeCode": "001",
                                    "roadTypeAbbName": "string",
                                    "roadName": self.address_street[:49],
                                    "townshipCode": self.address_post_code,
                                    # "townshipName": "string",
                                    "settlementTypeCode": "001",
                                    "settlementTypeAbbName": "string",
                                    "settlementName": self.address_province,
                                    "stateCode": "08",
                                    "stateAbbName": self.address_city,
                                    "zipCode": self.address_post_code,
                                    "countryCode": "484",
                                    "countryName": "MEX",
                                    "externalNum": "5201"
                                }
                            }
                        }
                    }
                }
            }

            # Convierte data a JSON
            data_json = json.dumps(data)

            response = requests.post(url=endpoint, headers=headers, data=data_json)  # Envía data_json en lugar de data

            print("Código de respuesta:", response.status_code)

            if response.status_code == 201:
                # Imprime la respuesta del servidor si es necesario
                print("Respuesta del servidor:", response.text)
            else:
                print("Respuesta del servidor:", response.text)


            response_json = response.json()
            return response_json

    
    def update_invoice(self):
        
        traking = self._tracking_estafeta()
        
        data = traking['data']
        weybill = traking['labelPetitionResult']['elements'][0]['wayBill']
        attachment_data = {
            'name': weybill,
            'datas': data,
            'res_model': 'account.move',  # Nombre del modelo actual
            'res_id': self.invoice_id.id,  # ID del registro actual
        }

        invoice = self.env['account.move'].browse(self.invoice_id.id)
        if invoice:
            invoice.write({
                'x_carrier_guide':weybill
            })


        
             

        





