from django.conf import settings
    
import datetime

from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER



class AppConfig(DjangoAppConfig):
    name = 'esr21_export'
    today_date = datetime.datetime.now().strftime('%Y%m%d')
    export_date =  '/documents/esr21_export_' + today_date
    subject_path = settings.MEDIA_ROOT + export_date + '/subject/'
    non_crf_path = settings.MEDIA_ROOT + export_date + '/non_crf/'
    metadata_path = settings.MEDIA_ROOT + export_date + '/metadata/'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Flourish Export'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = '99'
