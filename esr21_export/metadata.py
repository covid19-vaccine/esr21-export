import os, pandas as pd, openpyxl

from django.apps import apps as django_apps
from django.db.models import ForeignKey

class ExportMetadata:
    """Export data.
    """

    def __init__(self, export_path=None):
        self.export_path = export_path or django_apps.get_app_config('esr21_export').metadata_path
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)


    def generate_metadata(self, app_names=None):
        """Generate medata per app name for all models.
        """
        exclude_fields = []
        for app_name in app_names:
            app_models = django_apps.get_app_config(app_name).get_models()
            file_name = app_name + '.xlsx'
            final_path = self.export_path + file_name
            
            # Create file
            wb = openpyxl.Workbook()            
            wb.save(final_path)
            
            for app_model in app_models:
                sheet_name = app_model._meta.label_lower
                sheet_name = sheet_name.split('.')[1]
                model_data = [['variable name', 'Question']]
                for field_object in app_model._meta.get_fields():
                    if not isinstance(field_object, ForeignKey) and field_object.name not in exclude_fields:
                        try:
                            model_data.append([field_object.name, field_object.verbose_name])
                        except AttributeError:
                            pass
                df = pd.DataFrame(model_data)
                with pd.ExcelWriter(final_path, mode='a') as writer:  
                    df.to_excel(writer, sheet_name=sheet_name, engine='xlsxwriter')