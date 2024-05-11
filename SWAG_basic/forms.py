from django import forms
from SWAG_basic.models import *


class VolunteerForm(forms.ModelForm):

    name = forms.CharField(help_text='Enter full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter full name',
            'class': 'form-control',
        }
    ))

    email = forms.CharField(help_text='Enter email address', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter quantity',
            'class': 'form-control ',
            'type': 'email'
        }
    ))

    phone_number = PhoneNumberField(region="NG", help_text='Enter Phone number')

    occupation = forms.CharField(help_text='Enter occupation', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter occupation',
            'class': 'form-control ',
        }
    ))

    age = forms.CharField(help_text='Enter your age', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter your age',
            'class': 'form-control',
            'type': 'number',
        }
    ))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="(Select Your Gender)", required=True, help_text="Select Your Gender", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    role_you_want_to_volunteer = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label="(Select the role you want to volunteer)", required=True, help_text="In what role do you want to volunteer?", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    other_role = forms.CharField(help_text='Any other role, please specify.', required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'other role',
            'class': 'form-control ',
        }
    ))

    school = forms.CharField(help_text='Are you a teacher?, if yes enter the school where you are teaching', required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter school',
            'class': 'form-control ',
        }
    ))

    class Meta:
        model = Volunteer
        fields = ('name', 'email', 'phone_number', 'occupation', 'age', 'gender', 'role_you_want_to_volunteer', 'other_role', 'school')


class TrainingForm(forms.ModelForm):

    name = forms.CharField(help_text='Enter full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter full name',
            'class': 'form-control',
        }
    ))

    email = forms.CharField(help_text='Enter email address', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter quantity',
            'class': 'form-control ',
            'type': 'email'
        }
    ))

    phone_number = PhoneNumberField(region="NG", help_text='Enter Phone number')

    occupation = forms.CharField(help_text='Enter occupation', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter occupation',
            'class': 'form-control ',
        }
    ))

    age = forms.IntegerField(help_text='Enter your age', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter your age',
            'class': 'form-control ',
        }
    ))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="(Select Your Gender)", required=True, help_text="Select Your Gender", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = Training
        fields = ('name', 'email', 'phone_number', 'occupation', 'age', 'gender')