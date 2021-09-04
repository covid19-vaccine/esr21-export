from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'esr21_export' else False

esr21_export = Navbar(name='esr21_export')

esr21_export.append_item(
    NavbarItem(name='study_data_export',
               label='Data Export',
               fa_icon='fa-cogs',
               url_name='esr21_export:home_url'))

esr21_export.append_item(
    NavbarItem(
        name='export_data',
        title='Export Data',
        label='ESR21 Export Data',
        fa_icon='fa fa-database',
        url_name=settings.DASHBOARD_URL_NAMES[
            'export_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(esr21_export)
