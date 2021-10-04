from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'email', 'is_staff', 'is_active', 'full_name', 'phone_number', 'user_type')
    list_filter = ('id', 'email', 'is_staff', 'is_active', 'full_name', 'phone_number', 'user_type')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'phone_number', 'address', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2', 'phone_number', 'address', 'is_staff', 'is_active', 'user_type')}
        ),
    )
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
