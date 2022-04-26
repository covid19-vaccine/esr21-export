import datetime
import re

from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django_crypto_fields.fields import (
    EncryptedCharField, EncryptedDecimalField, EncryptedIntegerField,
    EncryptedTextField, FirstnameField, IdentityField, LastnameField)
from pytz import timezone

from esr21_subject.models import SeriousAdverseEventRecord

encrypted_fields = [
    EncryptedCharField, EncryptedDecimalField, EncryptedIntegerField,
    EncryptedTextField, FirstnameField, IdentityField, LastnameField]


class ExportMethods:
    """Export ESR21 data.
    """

    def __init__(self):
        self.rs_cls = django_apps.get_model('edc_registration.registeredsubject')
        self.subject_consent_csl = django_apps.get_model('esr21_subject.informedconsent')
        self.onschedule_cls = django_apps.get_model('esr21_subject.onschedule')

    def encrypt_values(self, obj_dict=None, obj_cls=None):
        """Ecrypt values for fields that are encypted.
        """
        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            for f in obj_cls._meta.get_fields():
                if key == f.name and type(f) in encrypted_fields:
                    new_value = f.field_cryptor.encrypt(value)
                    result_dict_obj[key] = new_value
        return result_dict_obj

    def get_participant_cohort(self, subject_identifier):

        onschedule_objs = self.onschedule_cls.objects.filter(
            subject_identifier=subject_identifier)

        if onschedule_objs:
            onschedule_obj = onschedule_objs[0]
            if 'sub' in onschedule_obj.schedule_name:
                return 'sub cohort'
            else:
                return 'main cohort'

    def fix_date_format(self, obj_dict=None):
        """Change all dates into a format for the export
        and split the time into a separate value.

        Format: m/d/y
        """

        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            if isinstance(value, datetime.datetime):
                value = value.astimezone(timezone('Africa/Gaborone'))
                time_value = value.time().strftime('%H:%M:%S.%f')
                time_variable = None
                if 'datetime' in key:
                    time_variable = re.sub('datetime', 'time', key)
                elif 'vaccination_date' == key:
                    time_variable = re.sub('date', 'time', key)
                else:
                    time_variable = key + '_time'
                value = value.strftime('%m/%d/%Y')
                new_key = re.sub('time', '', key)
                result_dict_obj[new_key] = value
                if not 'vaccination_date':
                    del result_dict_obj[key]
                result_dict_obj[time_variable] = time_value
            elif isinstance(value, datetime.date):
                value = value.strftime('%m/%d/%Y')
                result_dict_obj[key] = value
        return result_dict_obj

    def subject_crf_data_dict(self, crf_obj=None):
        """Return a crf obj dict adding extra required fields.
        """

        data = crf_obj.__dict__
        data = self.encrypt_values(obj_dict=data, obj_cls=crf_obj.__class__)
        if crf_obj.__class__ == SeriousAdverseEventRecord:
            data.update(
                subject_identifier=crf_obj.serious_adverse_event.subject_visit.subject_identifier,
                visit_datetime=crf_obj.serious_adverse_event.subject_visit.report_datetime,
                last_alive_date=crf_obj.serious_adverse_event.subject_visit.last_alive_date,
                reason=crf_obj.serious_adverse_event.subject_visit.reason,
                survival_status=crf_obj.serious_adverse_event.subject_visit.survival_status,
                visit_code=crf_obj.serious_adverse_event.subject_visit.visit_code,
                visit_code_sequence=crf_obj.serious_adverse_event.subject_visit.visit_code_sequence,
                study_status=crf_obj.serious_adverse_event.subject_visit.study_status,
                appt_status=crf_obj.serious_adverse_event.subject_visit.appointment.appt_status,
                appt_datetime=crf_obj.serious_adverse_event.subject_visit.appointment.appt_datetime,
            )
            try:
                rs = self.rs_cls.objects.get(subject_identifier=crf_obj.serious_adverse_event.subject_visit.subject_identifier)
            except self.rs_cls.DoesNotExist:
                raise ValidationError('RegisteredSubject can not be missing')
            else:
                data.update(
                    screening_age_in_years=rs.screening_age_in_years,
                    registration_status=rs.registration_status,
                    dob=rs.dob,
                    gender=rs.gender,
                    subject_type=rs.subject_type,
                    registration_datetime=rs.registration_datetime,
                )
        else:
            data.update(
                subject_identifier=crf_obj.subject_visit.subject_identifier,
                visit_datetime=crf_obj.subject_visit.report_datetime,
                last_alive_date=crf_obj.subject_visit.last_alive_date,
                reason=crf_obj.subject_visit.reason,
                survival_status=crf_obj.subject_visit.survival_status,
                visit_code=crf_obj.subject_visit.visit_code,
                visit_code_sequence=crf_obj.subject_visit.visit_code_sequence,
                study_status=crf_obj.subject_visit.study_status,
                appt_status=crf_obj.subject_visit.appointment.appt_status,
                appt_datetime=crf_obj.subject_visit.appointment.appt_datetime,
            )
            try:
                rs = self.rs_cls.objects.get(subject_identifier=crf_obj.subject_visit.subject_identifier)
            except self.rs_cls.DoesNotExist:
                raise ValidationError('RegisteredSubject can not be missing')
            else:
                data.update(
                    screening_age_in_years=rs.screening_age_in_years,
                    registration_status=rs.registration_status,
                    dob=rs.dob,
                    gender=rs.gender,
                    subject_type=rs.subject_type,
                    registration_datetime=rs.registration_datetime,
                )
        return data

    def non_crf_obj_dict(self, obj=None):
        """Return a dictionary of non crf object.
        """

        data = obj.__dict__
        data = self.encrypt_values(obj_dict=data, obj_cls=obj.__class__)
        subject_consent = self.subject_consent_csl.objects.filter(subject_identifier=obj.subject_identifier).last()
        if subject_consent:
            if 'dob' not in data:
                data.update(dob=subject_consent.dob)
            if 'gender' in data:
                data.update(gender=subject_consent.gender)
            if 'screening_identifier' not in data:
                data.update(screening_identifier=subject_consent.screening_identifier)
        else:
            if 'screening_identifier' not in data:
                data.update(screening_identifier=None)
            data.update(
                screening_age_in_years=None,
                dob=None,
                gender=None,
            )
        if 'registration_datetime' not in data:
            try:
                rs = self.rs_cls.objects.get(subject_identifier=obj.subject_identifier)
            except self.rs_cls.DoesNotExist:
                data.update(
                    registration_datetime=None,
                    screening_datetime=None
                )
            else:
                data.update(
                    registration_datetime=rs.registration_datetime,
                    screening_datetime=rs.screening_datetime
                )
        return data
