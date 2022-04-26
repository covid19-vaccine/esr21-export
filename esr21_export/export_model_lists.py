exclude_fields = [
    'created', '_state', 'hostname_created', 'hostname_modified', 'revision',
    'device_created', 'device_modified', 'id', 'created_time',
    'modified_time', 'report_datetime_time', 'registration_datetime_time',
    'screening_datetime_time', 'modified', 'form_as_json', 'consent_model',
    'randomization_datetime', 'registration_datetime', 'is_verified_datetime',
    'first_name', 'last_name', 'initials', 'guardian_name', 'identity',
    'infant_visit_id', 'maternal_visit_id', 'processed', 'processed_datetime',
    'packed', 'packed_datetime', 'shipped', 'shipped_datetime',
    'received_datetime', 'identifier_prefix', 'primary_aliquot_identifier',
    'clinic_verified', 'clinic_verified_datetime', 'drawn_datetime',
    'related_tracking_identifier', 'parent_tracking_identifier', 'provider_name']

exclude_m2m_fields = exclude_fields + ['display_index', 'field_name',
                                       'name', 'version']

subject_crfs_list = [
    'adverseevent',
    'concomitantmedication',
    'covid19preventativebehaviours',
    'covid19symptomaticinfections',
    'hospitalisation',
    'demographicsdata',
    'medicalhistory',
    'physicalexam',
    'pregnancystatus',
    'pregnancytest',
    'rapidhivtesting',
    'samplecollection',
    'specialinterestadverseevent',
    'targetedphysicalexamination',
    'vaccinationdetails',
    'vitalsigns',
    'covid19results'
]

subject_inlines_dict = {
    'adverseevent': [['adverseeventrecord'], 'adverse_event_id'],
    'seriousadverseevent': [
        ['seriousadverseeventrecord'], 'serious_adverse_event_id'],
    'specialinterestadverseevent': [
        ['specialinterestadverseeventrecord'], 'special_interest_adverse_event_id'], 
}

subject_model_list = [
    'eligibilityconfirmation', 'screeningeligibility', 'informedconsent',
    'personalcontactinfo', 'seriousadverseevent', 'specialinterestadverseevent',
    'subjectrequisition', 'subjectvisit'
]

subject_many_to_many_crf = [
    ['hospitalisation', 'covid_symptoms', 'covidsymptoms'],
    ['medicalhistory', 'covid_symptoms', 'symptoms'],
    ['medicalhistory', 'comorbidities', 'diseases'],
    ['pregnancystatus', 'contraceptive', 'contraception'],
    ['seriousadverseeventrecord', 'sae_criteria', 'saecriteria'],
]

subject_many_to_many_non_crf = []

offstudy_prn_model_list = ['subjectoffstudy', ]


death_report_prn_model_list = ['deathreport', ]
