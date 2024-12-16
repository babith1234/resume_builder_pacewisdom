from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'summary', 'phone_number','email' 'technical_skills']

    technical_skills = forms.JSONField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 40}), required=True)
