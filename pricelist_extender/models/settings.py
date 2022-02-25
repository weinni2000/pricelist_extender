# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    activate_module = fields.Boolean(
        "Activate Custom Price Lists", default=True)

    show_categories = fields.Boolean(
        "Show Categories", default=True)

    show_recommended_prices = fields.Boolean(
        "Show List Prices", default=True)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            show_categories=self.env['ir.config_parameter'].sudo().get_param(
                'pricelist_extender.show_categories'),
            show_recommended_prices=self.env['ir.config_parameter'].sudo().get_param(
                'pricelist_extender.show_recommended_prices'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        param.set_param('pricelist_extender.show_categories',
                        self.show_categories)
        param.set_param(
            'pricelist_extender.show_recommended_prices', self.show_recommended_prices)
