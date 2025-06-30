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

        with transaction.atomic():  # Ensures both User and Company_profile are created together
            user = self.create_user(username, password, **extra_fields)

            # Prompt for additional Company_profile details
            from Employee_Management.models import Company_profile
            
            print("\n--- Enter SuperAdmin Profile Details ---")
            empid = input("Employee ID: ")
            name = input("Full Name: ")
            mobileno = input("Mobile Number: ")
            email = input("Email: ")
            emergency_no = mobileno
            date_of_joining = datetime.now()
            

            # Create Company Profile
            Company_profile.objects.create(
                empid=empid,
                name=name,
                mobileno=mobileno,
                email=email,
                emergency_no=emergency_no,
                date_of_joining=date_of_joining,
            )

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
