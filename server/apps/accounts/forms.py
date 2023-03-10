import logging
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, UsernameField
from django.core.mail import send_mail

from apps.accounts.models import User

logger = logging.getLogger(__name__)


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # field_classes = {'email': UsernameField}

    def send_mail(self):
        logger.info(
            f"Sending signup email for email={self.cleaned_data['email']}")

        message = "Welcome {}".format(self.cleaned_data['email'])

        send_mail("Welcome to BookTime", message, "site@booktime.domain",
                  [self.cleaned_data['email']], fail_silently=True)


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, strip=False)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user = authenticate(
                self.request, email=email, password=password)

            if self.user is None:
                raise forms.ValidationError(
                    "Invalid email/password combination.")

            logger.info(f"Authentication successful for email {email}")

        return self.cleaned_data

    def get_user(self):
        return self.user


class CustomeProfileInput(forms.widgets.FileInput):
    template_name = 'form/image_preview.html'


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile', 'username', 'first_name', 'last_name')
        widgets = {
            'profile': CustomeProfileInput()
        }

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if not first_name and not last_name:
            raise forms.ValidationError(
                "Please provide your first name and your last name.")

        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            user = User.objects.exclude(pk=self.instance.pk).get(
                username__iexact=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(f"Username {user} already in user.")


class EmailEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError(f"Email {user} already in use.")
