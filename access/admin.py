from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import forms

from .models import User


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Groups', {'fields': ('groups', 'user_permissions',)}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )

    list_display = ('email', )
    list_filter = ('is_active', )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
