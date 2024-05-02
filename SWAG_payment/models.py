from django.db import models
from SWAG_auth.models import User
import uuid

# Create your models here.

class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    product_name = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    picture = models.ImageField(upload_to='uploads/', null=True)

    def __str__(self):
        return f'{self.product_name} | {self.amount}'

    class Meta:
        db_table = 'Product'
        verbose_name_plural = "Product"

class Payments(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    tx_ref = models.CharField(max_length=500)
    transaction_id = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    amount = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=500)

    user = models.ForeignKey(to="SWAG_auth.User", blank=True, null=True, on_delete=models.CASCADE)
    school = models.ForeignKey(to="Schools", blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name='date_created', auto_now=True, null=True)

    def __str__(self):
        return f'{self.user} | {self.amount}'


    class Meta:
        db_table = 'Payments'
        verbose_name_plural = "Payments"

class PaymentReceipt(models.Model):
    receipt_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    payment_receipt = models.FileField(upload_to='receipt/', null=True)
    user = models.ForeignKey(to="SWAG_auth.User", blank=True, null=True, on_delete=models.CASCADE, related_name="user_payment_receipt")
    status = models.CharField(max_length=500, default="pending")
    date_uploaded = models.DateTimeField(verbose_name='date_uploaded', auto_now=True, null=True)

    def __str__(self):
        return f'{self.user} | has uploaded a receipt'

    class Meta:
        db_table = 'Payment Receipt'
        verbose_name_plural = "Payment Receipts"

class States(models.Model):
    state = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.state}'

    class Meta:
        db_table = 'States'
        verbose_name_plural = "States"

class Schools(models.Model):
    school_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    school_name = models.CharField(max_length=500)
    state = models.ForeignKey(States, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.school_name} | {self.state}'

    class Meta:
        db_table = 'School'
        verbose_name_plural = "Schools"