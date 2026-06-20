from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.account.models import Account, Address


class AddressCreationForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'region', 'state', 'zip_code']

class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'phone']

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'region', 'state', 'zip_code']

class AccountUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'phone']