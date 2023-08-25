from django.contrib.auth.base_user import BaseUserManager
from organization.models import Organization

# from .models import EmployeeInformation


class UserManager(BaseUserManager):
    """
    This is the manager for custom user model
    """

    def create_user(self, email: str = "", password=None):
        if not email:
            raise ValueError("Email should not be empty")

        if not password:
            raise ValueError("Password should not be empty")

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        org = Organization.objects.create(name="Main")
        user.save(using=self._db)
        user.employee_information_user.organization = org
        user.employee_information_user.save()
        return user
