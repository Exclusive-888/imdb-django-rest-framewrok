from django import forms

from .models import Celebrity


class CelebrityForm(forms.ModelForm):
    class Meta:
        model = Celebrity
        fields = '__all__'
        widgets = {
            'duties': forms.CheckboxSelectMultiple
        }


