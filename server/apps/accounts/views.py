import logging
import http

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from apps.accounts.forms import UserCreationForm, PersonalInfoForm, EmailEditForm
from apps.accounts.models import User

logger = logging.getLogger(__name__)

# Create your views here.


class SignupView(FormView):
    template_name = 'accounts/registration/signup.html'
    form_class = UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get('next', '/')
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)

        form.save()

        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')

        logger.info(f"New signup for email={email} through SignupView")

        user = authenticate(self.request, email=email, password=raw_password)
        login(self.request, user=user)

        form.send_mail()

        messages.success(self.request, "You signed up successfully.")

        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user/profile.html'
    # permission_required = 'accounts.view_user'


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user/settings.html'


def info_edit_view(request):
    current_user = get_object_or_404(User, pk=request.user.pk)

    if request.method == 'POST':
        form = PersonalInfoForm(
            request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Personal information updated successfully")
            return redirect('accounts:edit_info')
        status = http.HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        status = http.HTTPStatus.OK
        form = PersonalInfoForm(instance=current_user)

    return render(request, 'accounts/user/edit_personal_info.html', {
        'form': form
    }, status=status)


def email_edit_view(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = EmailEditForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Email changed successfully")
            return redirect('accounts:edit_info')
        status = http.HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        status = http.HTTPStatus.OK
        form = EmailEditForm(instance=current_user)

    return render(request, 'accounts/user/edit_email.html', {'form': form}, status=status)


class EditPasswordView(PasswordChangeView):
    template_name = 'accounts/user/edit_password.html'
    success_url = reverse_lazy('accounts:settings')


class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user/settings.html'
