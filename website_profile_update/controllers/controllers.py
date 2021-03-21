import base64
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerProfile(CustomerPortal):

    CustomerPortal.MANDATORY_BILLING_FIELDS.append("image_1920")

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):

        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)

            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key]
                               for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                values.update({'country_id': int(values.pop('country_id', 0))})
                values.update({'zip': values.pop('zipcode', '')})
                if values.get('state_id') == '':
                    values.update({'state_id': False})
                values['image_1920'] = False
                files_to_send = request.httprequest.files.getlist('image_1920')
                for file in files_to_send:
                    values['image_1920'] = base64.b64encode(file.read())
                partner.sudo().write(values)
                if values.get('image_1920'):
                    request.env.user.sudo().write({'image_1920': values.get('image_1920')})
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
