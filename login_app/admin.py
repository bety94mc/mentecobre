from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import CheckboxSelectMultiple

from import_export.admin import ImportExportModelAdmin

from .models import CustomUser, Universe

# Register your models here.

class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):

    list_display = ('id', 'username')

    fieldsets = ((None, {'fields': ('username', 'password')}),
                 ('Extra Info', {'fields': ('rol', 'universe')}),
                 ('Permisos', {'fields': ('groups', 'is_superuser', 'is_staff', 'is_active', 'is_resting')}),
                 ('Fechas',{'fields':('date_joined','timeoff_date','out_date')})
                 )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Universe)
class UniverseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'universe')

admin.site.site_header = "Nave Nodriza"
admin.site.site_title = "Mandos Nave Nodriza"