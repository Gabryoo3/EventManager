from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from apps.account.models import Account
from apps.account.models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'city', 'state', 'zip_code')
    search_fields = ('street_address', 'city', 'state', 'zip_code')
@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'is_organizer', 'created_at')
    list_filter = ('is_organizer',)
    readonly_fields = tuple(UserAdmin.readonly_fields or ()) + ('created_at',)

    fieldsets = tuple(UserAdmin.fieldsets or ()) + (
        ('Extra Info', {
            'fields': ('birth_date', 'address', 'phone','is_organizer', 'created_at')
        }),
    )
    add_fieldsets = tuple(UserAdmin.add_fieldsets or ()) + (
        ('Extra Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'birth_date', 'email', 'phone', 'address', 'is_organizer',)
        }),
    )

class OrganizerAdminForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        is_organizer = cleaned_data.get('is_organizer')
        stage_name = cleaned_data.get('stage_name')
        main_category = cleaned_data.get('main_category')
        if is_organizer and not main_category and not stage_name:
            raise forms.ValidationError("Organizers must have a main category and stage name.")
        return cleaned_data