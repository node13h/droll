# Copyright (C) 2017 Sergej Alikov <sergej.alikov@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm, UserChangeForm


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password', 'two_fa_enabled')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Groups'), {'fields': ('groups', 'user_permissions',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )

    list_display = ('email', )
    list_filter = ('is_active', )
    search_fields = ('email',)
    ordering = ('email',)
