from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager
from core.models import BaseModel
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model Class
    """

    email = models.EmailField(unique=True, verbose_name="Email", blank=False)

    is_staff = models.BooleanField(
        verbose_name="Staff Status",
        default=False,
        help_text="Designate if the user has " "staff status",
    )
    is_active = models.BooleanField(
        verbose_name="Active Status",
        default=True,
        help_text="Designate if the user has " "active status",
    )
    is_superuser = models.BooleanField(
        verbose_name="Superuser Status",
        default=False,
        help_text="Designate if the " "user has superuser " "status",
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-id"]


class EmployeeInformation(BaseModel):
    """
    Model for Employee Information
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_information_user"
    )
    organization = models.ForeignKey(
        "organization.Organization",
        related_name="employee_organization",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    nid_number = models.CharField(max_length=100, null=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(verbose_name="Birth Date", blank=True, null=True)
    gender_options = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    gender = models.CharField(
        verbose_name="Choose Gender", choices=gender_options, max_length=20, null=True
    )

    def __str__(self):
        return f"{self.id} | {self.first_name} {self.last_name}"


@receiver(post_save, sender=User)
def create_instances(sender, instance, created, **kwargs):
    if created:
        EmployeeInformation.objects.create(user=instance)
