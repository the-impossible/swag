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


STATUS_CHOICES =(
("pending", "pending"),
("success", "success"),
# ("failed", "failed"),
)

class VerifyUploadedReceiptForm(forms.ModelForm):

    transaction_id = forms.CharField(help_text='Enter transaction id', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter transaction id',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    quantity = forms.IntegerField(help_text='Enter quantity', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter quantity',
            'class': 'form-control form-control-lg input-lg',
            'type': 'number'
        }
    ))

    status = forms.ChoiceField(choices=STATUS_CHOICES)


    class Meta:
        model = Payments
        fields = ('transaction_id', 'quantity', 'status')


"""
    transaction_id = models.CharField(max_length=500, blank=True, null=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=500)
"""