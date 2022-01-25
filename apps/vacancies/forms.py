import json

from django import forms

from apps.vacancies.models import Vacancy, VacancySkills


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('name', 'experience', 'price_min', 'price_max', 'skills', 'description')

    name = forms.CharField(min_length=1, max_length=128, required=True, label="Название вакансии")
    experience = forms.ChoiceField(choices=Vacancy.EXPERIENCE, label='Требуемый опыт работы',
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    price_min = forms.IntegerField(required=False, label='от')
    price_max = forms.IntegerField(required=False, label='до')
    description = forms.CharField(max_length=5000, label='Описание вакансии',
                                  widget=forms.Textarea(attrs={'class': '', 'rows': 15}))
    # company = forms.IntegerField(required=False, widget=forms.HiddenInput, label='Организация')
    skills = forms.CharField(required=False, label='Ключевые навыки', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # vacancy_id = args[0].get('id') if args and args[0] else None

        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-select'
                field.help_text = ''
            else:
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''

    def clean_price_min(self, field_name='price_min'):
        try:
            value = self.cleaned_data[field_name]
            if value:
                return int(value) if int(value) > 0 else None
        except forms.ValidationError as _:
            raise forms.ValidationError('Не корректное значение размера заработной платы')
        return None

    def clean_price_max(self):
        return self.clean_price_min(field_name='price_max')

    def save(self, commit=True, company=None):
        try:
            vacancy = super().save(commit=False)
            if commit:
                if not hasattr(vacancy, 'company'):
                    vacancy.company = company
                vacancy.save()

                # Закидываем ключевые навыки
                VacancySkills.objects.filter(vacancy=vacancy).delete()
                for i in json.loads(self.cleaned_data['skills'] or '[]'):
                    VacancySkills.objects.create(vacancy=vacancy, name=i['value'])
            return vacancy
        except Exception as e:
            raise e
