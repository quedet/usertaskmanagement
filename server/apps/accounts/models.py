from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
# Create your models here.


class UserManager(BaseUserManager):
    def _create(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email address must be set")

        user = self.model(email=self.normalize_email(email),
                          username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create(username, email, password, **extra_fields)


def get_profile_image_pathname(self, filename):
    print(filename)
    return f"profile/{self.pk}/{self.username}_{timezone.now()}_n.png"


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField('Email address', unique=True)

    profile = models.ImageField(
        blank=True, upload_to=get_profile_image_pathname, default='default/44884218_345707102882519_2446069589734326272_n.jpg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
