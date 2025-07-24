from django import forms
from django.forms import ModelForm
from . models import employee_groups

class add_emp(ModelForm):
    class Meta:
        model=employee_groups
        fields='__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'ifid': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'entity': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
           
        }