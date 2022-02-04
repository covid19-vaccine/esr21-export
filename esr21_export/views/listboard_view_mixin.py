import datetime
import os
import shutil
import threading
import time

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from edc_base.utils import get_utcnow

from ..export_data_mixin import ExportDataMixin
from ..export_methods import ExportMethods
from ..export_model_lists import (
    subject_crfs_list, subject_inlines_dict, subject_many_to_many_crf,
    subject_model_list, death_report_prn_model_list,
    offstudy_prn_model_list, subject_many_to_many_non_crf)
from ..metadata_app_names_list import metadata_app_names
from ..export_non_crfs import ExportNonCrfData
from ..metadata import ExportMetadata
from ..models import ExportFile


class ListBoardViewMixin:

    def export_subject_data(self, export_path=None):
            """Export all subject CRF data.
            """
            export_crf_data = ExportDataMixin(export_path=export_path)
            export_crf_data.export_crfs(
                crf_list=subject_crfs_list,
                crf_data_dict=ExportMethods().subject_crf_data_dict,
                study='esr21_subject')
            export_crf_data.export_inline_crfs(
                inlines_dict=subject_inlines_dict,
                crf_data_dict=ExportMethods().subject_crf_data_dict,
                study='esr21_subject')
            export_crf_data.generate_m2m_crf(
                m2m_class=subject_many_to_many_crf,
                crf_data_dict=ExportMethods().subject_crf_data_dict,
                study='esr21_subject')

    def export_non_crf_data(self, export_path=None):
        """Export subject non CFR data.
        """
        non_crf_data = ExportNonCrfData(export_path=export_path)
        non_crf_data.death_report(death_report_prn_model_list=death_report_prn_model_list)
        non_crf_data.subject_non_crfs(subject_model_list=subject_model_list)
        non_crf_data.subject_m2m_non_crf(subject_many_to_many_non_crf=subject_many_to_many_non_crf)
        non_crf_data.subject_visit()
        non_crf_data.offstudy(offstudy_prn_model_list=offstudy_prn_model_list)

    def export_metadat_data(self, export_path=None):
        """Export metadata.
        """
        metadata = ExportMetadata(export_path=export_path)
        metadata.generate_metadata(app_names=metadata_app_names)

    def export_requisitions(self, subject_export_path=None):
        """Export subject requisitions.
        """
        pass

    def download_all_data(self):
        """Export all data.
        """

        export_identifier = self.identifier_cls().identifier
        thread_name = 'esr21_all_export'
        last_doc = ExportFile.objects.filter(
            description='ESR21 All Export', download_complete=True).order_by(
                'created').last()

        if last_doc:
            download_time = last_doc.download_time
        else:
            download_time = 0.0
        options = {
            'description': 'ESR21 All Export',
            'study': 'esr21',
            'export_identifier': export_identifier,
            'download_time': download_time
        }
        doc = ExportFile.objects.create(**options)
        try:
            start = time.perf_counter()
            today_date = datetime.datetime.now().strftime('%Y%m%d')

            zipped_file_path = 'documents/' + export_identifier + '_esr21_export_' + today_date + '.zip'
            dir_to_zip = settings.MEDIA_ROOT + '/documents/' + export_identifier + '_esr21_export_' + today_date

            export_path = dir_to_zip + '/subject/'
            self.export_subject_data(export_path=export_path)

            export_path = dir_to_zip + '/non_crf/'
            self.export_non_crf_data(export_path=export_path)

            doc.document = zipped_file_path
            doc.save()

            # Zip the file

            self.zipfile(
                thread_name=thread_name,
                dir_to_zip=dir_to_zip, start=start,
                export_identifier=export_identifier,
                doc=doc)
        except Exception as e:
            raise e

    def download_subject_data(self):
        """Export subject data.
        """

        export_identifier = self.identifier_cls().identifier
        thread_name = 'esr21_subject_crf_export'
        last_doc = ExportFile.objects.filter(
            description='ESR21 Subject CRF Export', download_complete=True).order_by(
                'created').last()

        if last_doc:
            download_time = last_doc.download_time
        else:
            download_time = 0.0
        options = {
            'description': 'ESR21 Subject CRF Export',
            'study': 'esr21',
            'export_identifier': export_identifier,
            'download_time': download_time
        }
        doc = ExportFile.objects.create(**options)
        try:
            start = time.perf_counter()
            today_date = datetime.datetime.now().strftime('%Y%m%d')

            zipped_file_path = 'documents/' + export_identifier + '_esr21_export_' + today_date + '.zip'
            dir_to_zip = settings.MEDIA_ROOT + '/documents/' + export_identifier + '_esr21_export_' + today_date

            export_path = dir_to_zip + '/subject/'
            self.export_subject_data(export_path=export_path)

            doc.document = zipped_file_path
            doc.save()

            # Zip the file

            self.zipfile(
                thread_name=thread_name,
                dir_to_zip=dir_to_zip, start=start,
                export_identifier=export_identifier,
                doc=doc)
        except Exception as e:
            raise e

    def download_non_crf_data(self):
        """Export all data.
        """
        export_identifier = self.identifier_cls().identifier
        thread_name = 'esr21_non_crf_export',
        last_doc = ExportFile.objects.filter(
            description='ESR21 Non CRF Export',
            download_complete=True).order_by('created').last()

        if last_doc:
            download_time = last_doc.download_time
        else:
            download_time = 0.0
        options = {
            'description': 'ESR21 Non CRF Export',
            'study': 'esr21',
            'export_identifier': export_identifier,
            'download_time': download_time
        }
        doc = ExportFile.objects.create(**options)
        try:
            start = time.perf_counter()
            today_date = datetime.datetime.now().strftime('%Y%m%d')

            zipped_file_path = 'documents/' + export_identifier + '_esr21_non_crf_export_' + today_date + '.zip'
            dir_to_zip = settings.MEDIA_ROOT + '/documents/' + export_identifier + '_esr21_non_crf_export_' + today_date

            export_path = dir_to_zip + '/non_crf/'
            self.export_non_crf_data(export_path=export_path)

            doc.document = zipped_file_path
            doc.save()

            # Zip the file

            self.zipfile(
                thread_name=thread_name,
                dir_to_zip=dir_to_zip, start=start,
                export_identifier=export_identifier,
                doc=doc)
        except Exception as e:
            raise e

    def download_medata(self):
        """Export all metadata.
        """

        export_identifier = self.identifier_cls().identifier
        thread_name = 'esr21_metadata_export',
        last_doc = ExportFile.objects.filter(
            description='Metadata Export',
            download_complete=True).order_by('created').last()

        if last_doc:
            download_time = last_doc.download_time
        else:
            download_time = 0.0
        options = {
            'description': 'Metadata Export',
            'study': 'esr21',
            'export_identifier': export_identifier,
            'download_time': download_time
        }
        doc = ExportFile.objects.create(**options)
        try:
            start = time.perf_counter()
            today_date = datetime.datetime.now().strftime('%Y%m%d')

            zipped_file_path = 'documents/' + export_identifier + '_esr21_metadata_export_' + today_date + '.zip'
            dir_to_zip = settings.MEDIA_ROOT + '/documents/' + export_identifier + '_esr21_metadata_export_' + today_date

            export_path = dir_to_zip + '/metadata/'
            self.export_metadat_data(export_path=export_path)

            doc.document = zipped_file_path
            doc.save()

            # Zip the file

            self.zipfile(
                thread_name=thread_name,
                dir_to_zip=dir_to_zip, start=start,
                export_identifier=export_identifier,
                doc=doc)
        except Exception as e:
            raise e

    def zipfile(
            self, thread_name=None, dir_to_zip=None, start=None,
            export_identifier=None, doc=None):
        """Zip file.
        """
        # Zip the file

        doc.download_complete = True
        doc.save()

        if not os.path.isfile(dir_to_zip):
            shutil.make_archive(dir_to_zip, 'zip', dir_to_zip)
            # Create a document object.

            end = time.perf_counter()
            download_time = end - start
            try:
                doc = ExportFile.objects.get(
                    export_identifier=export_identifier)
            except ExportFile.DoesNotExist:
                raise ValidationError('Export file is missing for id: ',
                                      export_identifier)
            else:
                doc.download_time = download_time
                doc.save()

            # Notify user the download is done
            subject = export_identifier + ' ' + doc.description
            message = (export_identifier + doc.description +
                       ' export files have been successfully generated and '
                       'ready for download. This is an automated message.')
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # FROM
                [self.request.user.email],  # TO
                fail_silently=False)
            threading.Thread(target=self.stop_main_thread, args=(thread_name,))

    def is_clean(self, description=None):

        current_file = ExportFile.objects.filter(
            description=description,
            download_complete=False).order_by('created').last()
        if current_file:
            time_now = (get_utcnow() - current_file.created).total_seconds()

            if time_now <= current_file.download_time:
                messages.add_message(
                    self.request, messages.INFO,
                    (f'Download for {description} that was initiated is still running '
                     'please wait until an export is fully prepared.'))
                return False

        # Delete any other extra failed files
        docs = ExportFile.objects.filter(download_complete=False)
        for doc in docs:
            if doc.created.date() < get_utcnow().date():
                doc.delete()
        return True

