# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2019-TODAY .
#    Author: Plementus <https://plementus.com>
#    Contributor: Mario Roshdy <m.roshdy@plementus.com>
#    Contributor: Karim Jaber <kareem@plementus.com>
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################

from odoo import http, _
import json
import logging

_logger = logging.getLogger(__name__)

class EinvoiceIntegration(http.Controller):
    def get_error_msg(self, exception):
        if hasattr(exception, 'name'):
            return exception.name
        elif hasattr(exception, 'content'):
            return exception.content
        elif hasattr(exception, 'args'):
            return exception.args
        elif hasattr(exception, 'pgerror'):
            return exception.pgerror


    @http.route('/api/v1/get_invoice', auth='public', type='json', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    def get_invoice(self, **kwargs):
        params = http.request.jsonrequest
        errors = []
        domain = []
        if 'invoice_id' in params and params.get('invoice_id'):
            id = params.get('invoice_id')
            domain.append(('id', '=', id))
        else:
            errors.append({'code': 1001, 'msg': "Invoice ID Is Mandatory!"})

        if errors:
            return {"errors": errors}

        try:
            invoice_id = http.request.env['account.move'].sudo().search(domain)
            if invoice_id:
                invoicemodel = invoice_id._prepare_eta_invoice()
                if 'signatures' in invoicemodel:
                    invoicemodel.pop("signatures")
                return {'data': invoicemodel}
            else:
                return {"errors": [{"code": 1002, 'msg': _("Invalid Invoice ID !")}]}
        except Exception as e:
            return {"errors": [{"code": 500, 'msg': self.get_error_msg(e)}]}


    @http.route('/api/v1/sign_invoice', auth='public', type='json', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    def sign_invoice(self, **kwargs):
        params = http.request.jsonrequest
        errors = []
        domain = []
        if 'invoice_id' in params and params.get('invoice_id'):
            id = params.get('invoice_id')
            domain.append(('id', '=', id))
        else:
            errors.append({'code': 1001, 'msg': "Invoice ID Is Mandatory !"})

        if 'signatures' not in params and not params.get('signatures'):
            errors.append({'code': 1003, 'msg': "Signatures Is Mandatory !"})

        if errors:
            return {"errors": errors}

        try:
            invoice_id = http.request.env['account.move'].sudo().search(domain)
            if invoice_id:
                signatures = params.get('signatures')
                signature = signatures[0]
                invoice_id.write({
                    'signature_type': str(signature.get("signatureType")),
                    'signature_value': str(signature.get("value")),
                    'eta_invoice_signed': True,
                })
                data = {'result': "Success"}
                return {'data': data}
            else:
                return {"errors": [{"code": 1002, 'msg': _("Invalid Invoice ID!")}]}
        except Exception as e:
            return {"errors": [{"code": 500, 'msg': self.get_error_msg(e)}]}
