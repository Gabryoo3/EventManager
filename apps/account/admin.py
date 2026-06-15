from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import Account
from apps.account.models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'city', 'state', 'zip_code')
    search_fields = ('street_address', 'city', 'state', 'zip_code')
@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'is_organizer')
    list_filter = ('is_organizer',)

    fieldsets = tuple(UserAdmin.fieldsets or ()) + (
        ('Extra Info', {
            'fields': ('birth_date', 'address', 'phone', 'is_organizer')
        }),
    )
    add_fieldsets = tuple(UserAdmin.add_fieldsets or ()) + (
        ('Extra Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'birth_date', 'email', 'phone', 'address', 'is_organizer')
        }),
    )