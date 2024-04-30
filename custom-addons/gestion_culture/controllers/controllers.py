# -*- coding: utf-8 -*-
# from odoo import http


# class GestionCulture(http.Controller):
#     @http.route('/gestion_culture/gestion_culture', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_culture/gestion_culture/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_culture.listing', {
#             'root': '/gestion_culture/gestion_culture',
#             'objects': http.request.env['gestion_culture.gestion_culture'].search([]),
#         })

#     @http.route('/gestion_culture/gestion_culture/objects/<model("gestion_culture.gestion_culture"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_culture.object', {
#             'object': obj
#         })

