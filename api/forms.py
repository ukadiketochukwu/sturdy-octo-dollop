from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Patient

# User registration form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}

# Doctor profile form
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty']

# Patient profile form
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth']
