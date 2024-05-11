from django.contrib import admin
from SWAG_basic.models import *

# Register your models here.
class TrainingAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'phone_number', 'occupation', 'age', 'gender')
    search_fields = ('name', 'email')
    ordering = ('-date_created',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class VolunteerAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'phone_number', 'occupation', 'age', 'gender', 'school', 'role_you_want_to_volunteer', 'other_role')
    search_fields = ('name', 'email')
    ordering = ('-date_created',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Training, TrainingAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Gender)
admin.site.register(Role)
