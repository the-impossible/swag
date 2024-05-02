from django import forms
from SWAG_payment.models import *


class UploadReceiptForm(forms.ModelForm):

    payment_receipt = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg, application/pdf'
        }
    ))

    class Meta:
        model = PaymentReceipt
        fields = ('payment_receipt',)


STATUS_CHOICES = (
    ("pending", "pending"),
    ("success", "success"),
    # ("failed", "failed"),
)

class VerifyUploadedReceiptForm(forms.ModelForm):

    transaction_id = forms.CharField(help_text='Enter transaction id', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter transaction id',
            'class': 'form-control ',
        }
    ))

    quantity = forms.IntegerField(help_text='Enter quantity', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter quantity',
            'class': 'form-control ',
            'type': 'number'
        }
    ))

    status = forms.ChoiceField(choices=STATUS_CHOICES)


    class Meta:
        model = Payments
        fields = ('transaction_id', 'quantity', 'status')

class CompeteForBoxForm(forms.Form):

    school = forms.ModelChoiceField(queryset=Schools.objects.all(), empty_label="(Select Your School)", required=True, help_text="Select Your School", widget=forms.Select(
        attrs={
            'class':'form-control',
            'name':'school',
        }
    ))

    quantity = forms.IntegerField(help_text='Enter quantity', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter quantity',
            'class': 'form-control square',
            'name': 'quantity'
        }
    ))


    def __init__(self, *args, **kwargs):
        state = kwargs.pop('state', '')

        super(CompeteForBoxForm, self).__init__(*args, **kwargs)
        self.fields['school'].queryset=Schools.objects.filter(state=States.objects.get(state=state))



