from django.contrib import admin
from SWAG_payment.models import *

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):

    list_display = ('tx_ref', 'transaction_id', 'description', 'amount', 'quantity', 'status', 'user_name', 'school')
    search_fields = ('user_name', 'school')
    ordering = ('-date_created',)

    def user_name(self, obj):
        return obj.user.name if obj.user else None

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PaymentReceiptAdmin(admin.ModelAdmin):

    list_display = ('payment_receipt', 'user_name', 'status', 'date_uploaded')
    search_fields = ('user_name', 'status')
    ordering = ('-date_uploaded',)

    def user_name(self, obj):
        return obj.user.name if obj.user else None

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Product)
admin.site.register(Payments, PaymentAdmin)
admin.site.register(PaymentReceipt)
admin.site.register(States)
admin.site.register(Schools)

