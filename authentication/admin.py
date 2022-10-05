from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.forms import CustomUserCreationForm, CustomUserChangeForm
from authentication.models import User, Booking

admin.site.site_header = "Stedom Admin"
admin.site.site_title = "Stedom"
admin.site.index_title = "Stedom"


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'full_name', 'specification', 'user_type', 'date_joined', 'rating')

    fieldsets = ((None,
                  {'fields': ('email', 'full_name', 'specification', 'user_type', 'rating', 'password',)}),
                 ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'specification', 'rating', 'password1', 'password2', 'is_staff', 'is_superuser',
                'is_active')}
         ),
    )
    search_fields = ('full_name', 'specification', 'email',)
    ordering = ('full_name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'date_time',
        'instructor',
        'learner',
    )
