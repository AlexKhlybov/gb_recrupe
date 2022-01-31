import datetime

from django import forms
from django.db import transaction

from apps.resume.models import Resume, ResumeSkills


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('name', 'price', 'about_me', 'skills', )

    name = forms.CharField(min_length=1, max_length=128, required=True, label="Желаемая должность")
    price = forms.IntegerField(required=False, label='Зарплата')
    skills = forms.CharField(required=False, label='Ключевые навыки', widget=forms.Textarea)
    about_me = forms.CharField(max_length=500, label='О себе', required=False,
                               widget=forms.Textarea(attrs={'class': '', 'rows': 4}))
    is_draft = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            skills = ', '.join([x.name for x in instance.skills])
            kwargs['initial'] = {'skills': skills, 'is_draft': instance.status == Resume.STATUS_DRAFT}
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-select'
                field.help_text = ''
            else:
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''


def get_resume_data(resume_id) -> dict:
    resume_data = {
        'experiences': [],  # Опыт работы
        'education': [],  # Образование
        'courses': [],  # Курсы
    }
    if resume_id:
        resume = Resume.objects.select_related().filter(pk=resume_id).first()

        # Опыт работы
        for i in resume.experience.all():
            resume_data['experiences'].append({
                'startMonth': i.start_date.month if i.start_date else None,
                'startYear': i.start_date.year if i.start_date else None,
                'endMonth': i.end_date.month if i.end_date else None,
                'endYear': i.end_date.year if i.end_date else None,
                'currentTimeFlag': not (i.end_date and i.end_date),

                'organisationName': i.organization_name,
                'positionName': i.position,
                'duties': i.duties,
            })

        # Образование
        for i in resume.education.all():
            resume_data['education'].append({
                'level': i.level,
                'institution': i.educational_institution,
                'faculty': i.faculty,
                'specialization': i.specialization,
                'yearOfEnding': i.year_of_ending,
            })

        # Курсы
        for i in resume.courses.all():
            resume_data['courses'].append({
                'institution': i.educational_institution,
                'faculty': i.faculty,
                'specialization': i.specialization,
                'yearOfEnding': i.year_of_ending,
            })

    return resume_data


def save_resume_data(request, resume_id, obj):
    with transaction.atomic():
        resume = Resume.objects.filter(pk=resume_id).first() if resume_id else Resume.objects.create(user=request.user)
        resume.name = obj['name']
        resume.price = obj['price']
        resume.about_me = obj['about_me']
        resume.status = Resume.STATUS_DRAFT if obj['draft'] else Resume.STATUS_PUBLIC
        resume.save()

        resume.experience.all().delete()
        for i in obj['experiences']:
            start_date = datetime.date(day=1, month=i['startMonth'], year=i['startYear']) \
                if i['startMonth'] and i['startYear'] else None
            end_date = datetime.date(day=1, month=i['endMonth'], year=i['endYear']) \
                if i['endMonth'] and i['endYear'] else None
            experience = {
                'start_date': start_date,
                'end_date': end_date,
                'organization_name': i['organisationName'],
                'position': i['positionName'],
                'duties': i['duties'],
            }
            resume.experience.create(**experience)

        resume.education.all().delete()
        for i in obj['education']:
            education = {
                'level': i['level'],
                'educational_institution': i['institution'],
                'faculty': i['faculty'],
                'specialization': i['specialization'],
                'year_of_ending': i['yearOfEnding'],
            }
            resume.education.create(**education)

        resume.courses.all().delete()
        for i in obj['courses']:
            courses = {
                'educational_institution': i['institution'],
                'faculty': i['faculty'],
                'specialization': i['specialization'],
                'year_of_ending': i['yearOfEnding'],
            }
            resume.courses.create(**courses)

        ResumeSkills.objects.filter(resume=resume).delete()
        for i in (i['value'] for i in obj['skills']):
            ResumeSkills.objects.create(resume=resume, name=i)
