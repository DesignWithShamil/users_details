from django import forms
from django.forms import ModelForm
from . models import empinfo

class empForm(ModelForm):
    class Meta:
        model=empinfo
        fields='__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'ifid': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'mobileno': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
           
        }