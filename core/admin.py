from django.contrib import admin
from .models import Licitacion, Preguntasbbdd, ErrorHistory
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(Licitacion)
admin.site.register(Preguntasbbdd)
admin.site.register(ErrorHistory)


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'rut')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'rut'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'rut', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'rut')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)