import pandas as pd

from django.apps import apps as django_apps


from .export_methods import ExportMethods


class ExportRequisitionData:
    """Export data.
    """

    def __init__(self, subject_export_path=None):
        self.subject_export_path = subject_export_path or django_apps.get_app_config('esr21_export').subject_path
        self.export_methods_cls = ExportMethods()