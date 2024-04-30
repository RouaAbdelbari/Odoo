from odoo import http, _
from odoo.http import request

class Reproduction(http.Controller):
    @http.route('/create_heat_period', auth='public', type='json', methods=['POST'])
    def create_heat_period(self, start_date, temperature, humidity, vache_id):
        try:
            # Créer une période de chaleur avec la date de début, la température, l'humidité et l'ID de la vache
            heat_period = request.env['reproduction.period'].create({
                'start_date': start_date,
                'temperature': temperature,
                'humidity': humidity,
                'vache_id': vache_id,
            })
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/confirm_heat_period', auth='public', type='json', methods=['POST'])
    def confirm_heat_period(self, heat_period_id):
        try:
            # Confirmer la période de chaleur
            heat_period = request.env['reproduction.period'].browse(heat_period_id)
            heat_period.action_confirm()
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}


