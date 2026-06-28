from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.AccountDetailView.as_view(), name='profile'),
    path('profile/update/profile/', views.AccountUpdateView.as_view(), name='update'),
    path('profile/update/address/', views.AddressUpdateView.as_view(), name='address_update'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='account/change_password.html',
        success_url=reverse_lazy('account:password_change_done')
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/change_password_done.html'
    ), name='password_change_done'),
    path('detail/<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
]