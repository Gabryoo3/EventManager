from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View

from apps.account.forms import AccountCreationForm, AddressCreationForm, AccountUpdateForm, AddressUpdateForm
from django.views.generic import DetailView, UpdateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.account.models import Account, Address
from apps.events.models import Event


# Create your views here.

class RegisterView(View):
    template_name = 'account/register_edit.html'
    success_message = 'Account creato con successo! Effettua il login per continuare.'
    def get(self, request, *args, **kwargs):
        account_form = AccountCreationForm()
        address_form = AddressCreationForm()
        return render(request, self.template_name, {
            'account_form': account_form,
            'address_form': address_form,
            'is_update' : False
        })

    def post(self, request, *args, **kwargs):
        account_form = AccountCreationForm(request.POST, request.FILES)
        address_form = AddressCreationForm(request.POST)
        if account_form.is_valid() and address_form.is_valid():
            address_instance = address_form.save()
            user = account_form.save(commit=False)
            user.address = address_instance
            user.save()
            messages.success(request, self.success_message)
            return redirect('account:login')
        return render(request, self.template_name, {
            'account_form': account_form,
            'address_form': address_form
        })

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/profile.html'
    context_object_name = 'account'
    def get_object(self):
        return Account.objects.select_related('address').get(pk=self.request.user.pk)

class AccountUpdateView(LoginRequiredMixin, View):
    template_name = 'account/register_edit.html'
    model = Account
    form_class = AccountUpdateForm
    success_message = 'Informazioni dell\'account aggiornate!'
    success_url = reverse_lazy('account:profile')
    def get(self, request, *args, **kwargs):
        account_form = self.form_class(instance=request.user)
        address_form = AddressUpdateForm(instance=request.user.address)
        return render(request, self.template_name, {
            'account_form': account_form,
            'address_form': address_form,
            'account': request.user,
            'is_update' : True
        })
    def post(self, request, *args, **kwargs):
        account_form = self.form_class(request.POST, request.FILES, instance=request.user)
        address_form = AddressUpdateForm(request.POST, instance=request.user.address)
        if account_form.is_valid() and address_form.is_valid():
            account_instance = account_form.save(commit=False)
            address_instance = address_form.save()
            account_instance.address = address_instance
            account_instance.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        return render(request, self.template_name, {
            'account_form': account_form,
            'address_form': address_form,
            'account': request.user
        })
    def get_object(self):
        return self.request.user

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/register_edit.html'
    model = Address
    form_class = AddressUpdateForm
    success_url = reverse_lazy('account:profile')
    def get_object(self):
        return self.request.user

class OrganizerDetailView(DetailView):
    model = Account
    template_name = 'account/organizer_detail.html'
    context_object_name = 'organizer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizer_events'] = Event.objects.filter(
            organizer=self.get_object(),
            date__gte=timezone.localdate()
        ).order_by('date')
        return context