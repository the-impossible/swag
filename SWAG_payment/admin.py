from django.contrib import admin
from SWAG_payment.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Payments)
admin.site.register(PaymentReceipt)
