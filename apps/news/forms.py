from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit
from django import forms

from apps.news.models import News


class NewsEditForm(forms.ModelForm):
    image = forms.ImageField(max_length=1024)

    class Meta:
        model = News
        exclude = ("created",)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8  mb-3"
        self.helper.layout = Layout(
            "title",
            "short_text",
            "text",
            "image",
            ButtonHolder(
                Submit('submit', 'Сохранить', css_class='bg-prymary  mt-5  text-white')
            )
        )
