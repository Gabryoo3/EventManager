
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.account.forms import AccountCreationForm, AddressCreationForm, AccountUpdateForm, AddressUpdateForm
from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.account.models import Account, Address

# Create your views here.

class RegisterView(View):
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        user_form = AccountCreationForm()
        address_form = AddressCreationForm()
        return render(request, self.template_name, {
            'user_form': user_form,
            'address_form': address_form
        })

    def post(self, request, *args, **kwargs):
        user_form = AccountCreationForm(request.POST)
        address_form = AddressCreationForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            address_instance = address_form.save()
            user = user_form.save(commit=False)
            user.address = address_instance
            user.save()
            return redirect('login')
        return render(request, self.template_name, {
            'user_form': user_form,
            'address_form': address_form
        })

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/profile.html'
    context_object_name = 'account'
    def get_object(self):
        return Account.objects.select_related('address').get(pk=self.request.user.pk)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/profile_edit.html'
    model = Account
    form_class = AccountUpdateForm
    success_url = reverse_lazy('account:profile')
    def get_object(self):
        return self.request.user

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/address_edit.html'
    model = Address
    form_class = AddressUpdateForm
    success_url = reverse_lazy('account:profile')
    def get_object(self):
        return get_object_or_404(Address, account=self.request.user)
    
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        account = get_object_or_404(Account, pk=request.user.pk)
        if request.user.is_organizer:
            return render(request, 'account/dashboard_organizer.html')
        return render(request, 'account/dashboard_attendee.html')
