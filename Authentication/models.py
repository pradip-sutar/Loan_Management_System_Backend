from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db import transaction
from datetime import datetime
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Removed Company_profile import and creation
        user = self.create_user(username, password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    license_key = models.CharField(max_length=255, blank=True, null=True)
    license_expiry = models.CharField(max_length=255, blank=True, null=True)
    is_license_valid = models.BooleanField(blank=True, null=True)
    # class UserType(models.TextChoices):
    #     ADMINUSER = 'Super Admin', 'Super Admin'
    #     GENERALUSER = 'generaluser', 'General User'

    # user_type = models.CharField(
    #     max_length=20,
    #     choices=UserType.choices,
    #     default=UserType.GENERALUSER
    # )

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
