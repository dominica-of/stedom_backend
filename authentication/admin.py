from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.forms import CustomUserCreationForm, CustomUserChangeForm
from authentication.models import User

admin.site.site_header = "Stedom Admin"
admin.site.site_title = "Stedom"
admin.site.index_title = "Stedom"


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'full_name', 'specification', 'date_joined')

    fieldsets = ((None,
                  {'fields': ('email', 'full_name', 'specification', 'password',)}),
                 ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'specification', 'password1', 'password2', 'is_staff', 'is_superuser',
                'is_active')}
         ),
    )
    search_fields = ('full_name', 'specification', 'email',)
    ordering = ('full_name',)