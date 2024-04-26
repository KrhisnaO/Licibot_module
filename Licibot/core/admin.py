from django.contrib import admin
from .models import Licitacion, Preguntasbbdd
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(Licitacion)
admin.site.register(Preguntasbbdd)


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'rut')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'rut', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'rut')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)