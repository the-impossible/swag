from django.contrib import admin
from SWAG_auth.models import *


# Register your models here.

class CustomAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'phone_number', 'address', 'state',)
    search_fields = ('name', 'email')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(User, CustomAdmin)

