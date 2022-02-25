from odoo import api, models


class ProductPricelistReportExtender(models.AbstractModel):
    _inherit = 'report.product.report_pricelist'

    def _get_report_data(self, data, report_type='html'):
        quantities = data['quantities'] or [1]

        pricelist_id = data['pricelist_id'] and int(
            data['pricelist_id']) or None
        pricelist = self.env['product.pricelist'].browse(pricelist_id).exists()
        if not pricelist:
            pricelist = self.env['product.pricelist'].search([], limit=1)

        active_model = data['active_model']
        active_ids = data.get('active_ids') or []
        is_product_tmpl = active_model == 'product.template'
        ProductClass = self.env[active_model]

        products = ProductClass.browse(
            active_ids) if active_ids else ProductClass.search([('sale_ok', '=', True)])
        products_data = [
            self._get_product_data(
                is_product_tmpl, product, pricelist, quantities)
            for product in products
        ]

        return {
            'is_html_type': report_type == 'html',
            'is_product_tmpl': is_product_tmpl,
            'is_visible_title': bool(data['is_visible_title']) or False,
            'pricelist': pricelist,
            'products': products_data,
            'quantities': quantities,
            "show_categories": self.env['ir.config_parameter'].get_param('pricelist_extender.show_categories'),
            "show_recommended_prices": self.env['ir.config_parameter'].get_param('pricelist_extender.show_recommended_prices')
        }

    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):

        data = {
            'id': product.id,
            'name': is_product_tmpl and product.name or product.display_name,
            "list_price": product.list_price,
            # get the variant price if exists otherwise take the template price
            "lst_price": getattr(product, 'lst_price', None) or product.list_price,
            'price': dict.fromkeys(quantities, 0.0),
            'uom': product.uom_id.name,
            'categ_id': product.categ_id.name or "no Cat"
        }
        # if "Customizable Desk" in data["name"]:
        #    print(data)

        for qty in quantities:
            data['price'][qty] = pricelist.get_product_price(
                product, qty, False)

        if is_product_tmpl and product.product_variant_count > 1:
            data['variants'] = [
                self._get_product_data(False, variant, pricelist, quantities)
                for variant in product.product_variant_ids
            ]

        return data

        return super()._get_report_data()
