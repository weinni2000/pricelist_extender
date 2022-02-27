###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import api, fields, models, _
from datetime import datetime


class ProductSeason(models.Model):
    _name = 'product.season'
    _description = 'Product season'
    _order = 'name'

    name = fields.Char(
        string='Name',
        translate=True,
        required=True)
    text_for_pricelist_manual = fields.Char(
        translate=True,
        required=False, default=False)
    text_for_pricelist_computed = fields.Char(
        compute='_compute_season_text')
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.user.company_id.id)
    date_from = fields.Date(
        string='From')
    date_to = fields.Date(
        string='To')
    product_tmpl_ids = fields.One2many(
        string='Products',
        comodel_name='product.template',
        inverse_name='season_id')
    product_tmpl_count = fields.Integer(
        string='Products count',
        compute='_compute_products_count')

    @api.depends('product_tmpl_ids')
    def _compute_products_count(self):
        for season in self:
            season.product_tmpl_count = len(self.product_tmpl_ids)

    @api.depends('text_for_pricelist_manual')
    def _compute_season_text(self):

        for text_for in self:
            aval = _("Available: ")
            if text_for.text_for_pricelist_manual == "" or text_for.text_for_pricelist_manual == False:
                try:
                    text_for.text_for_pricelist_computed = f"{aval}{datetime.strftime(text_for.date_from,'%d.%m.%Y')} -> {datetime.strftime(text_for.date_to,'%d.%m.%Y')}"
                except:
                    text_for.text_for_pricelist_computed = ""
            else:
                text_for.text_for_pricelist_computed = aval + text_for.text_for_pricelist_manual
