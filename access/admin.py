from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm


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
