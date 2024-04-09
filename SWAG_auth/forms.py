from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from SWAG_auth.models import *


class AccountCreationForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
        }
    ))

    password = forms.CharField(help_text='Enter Password', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'password',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    phone_number = PhoneNumberField(region="NG", help_text='Enter Phone number')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != None:
            if User.objects.filter(email=email.lower().strip()).exists():
                raise forms.ValidationError('Email Already taken!')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError("Password is too short!")

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number', 'password')

class UpdateUserCreationForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    phone_number = PhoneNumberField(region="NG", help_text='Enter Phone number')

    address = forms.CharField(help_text='Enter address', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter address',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number', 'address', 'picture')

class AdminCreationForm(AccountCreationForm, forms.ModelForm):

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone_number', 'picture')

class UpdateAdminForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'email',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    phone_number = PhoneNumberField(region="NG", help_text='Enter Phone number')


    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))
    

    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number', 'picture')

