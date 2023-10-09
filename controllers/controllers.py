# -*- coding: utf-8 -*-
# from odoo import http


# class EstafetaDelibery(http.Controller):
#     @http.route('/estafeta_delibery/estafeta_delibery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estafeta_delibery/estafeta_delibery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estafeta_delibery.listing', {
#             'root': '/estafeta_delibery/estafeta_delibery',
#             'objects': http.request.env['estafeta_delibery.estafeta_delibery'].search([]),
#         })

#     @http.route('/estafeta_delibery/estafeta_delibery/objects/<model("estafeta_delibery.estafeta_delibery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estafeta_delibery.object', {
#             'object': obj
#         })
