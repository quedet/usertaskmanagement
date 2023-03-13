from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

# from apps.accounts.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from apps.accounts.views import SignupView, ProfileView, SettingsView, info_edit_view, EditPasswordView, email_edit_view

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='accounts/registration/login.html',
                                     form_class=AuthenticationForm), name='login'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/settings/', SettingsView.as_view(), name='settings'),
    path('profile/settings/edit-personal-information',
         info_edit_view, name='edit_info'),
    path('profile/settings/edit-password/',
         EditPasswordView.as_view(), name='edit_password'),
    path('profile/settings/edit-email/',
         email_edit_view, name='edit_email'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/registration/password_reset_form.html',
        email_template_name='accounts/registration/password_reset_email.html',
        success_url='/accounts/password-reset/done/'), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/registration/password_reset_confirm.html',
        success_url='/accounts/password-reset/complete/'
    ), name='password_reset_confirm'),

    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/registration/password_reset_complete.html'
    ), name='password_reset_complete')
]
