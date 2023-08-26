from rest_framework import response, views, status, generics
from .models import User, EmployeeInformation
from .apipermissions import IsOwner, IsOrganizationAdmin
from .serializers import CreateUserSerializer
from django.shortcuts import get_object_or_404
from organization.models import Organization


class CreateOrganizationAdminView(generics.CreateAPIView):
    """
    Create Organization Admin API View
    """

    permission_classes = [IsOwner]
    serializer_class = CreateUserSerializer


class AddEmployeeView(generics.ListCreateAPIView):
    """
    Add Organization Employee API View
    """

    permission_classes = [IsOrganizationAdmin]
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        current_org = self.request.user.employee_information_user.organization

        if user_id := self.kwargs.get("id"):
            user = get_object_or_404(self.queryset, id=user_id)
            ser = self.serializer_class(user)
        else:
            user = self.queryset.filter(
                employee_information_user__organization=current_org
            )
            ser = self.serializer_class(user, many=True)

        return response.Response(ser.data)

    def create(self, request, *args, **kwargs):
        current_org = self.request.user.employee_information_user.organization
        data = self.request.data
        data["organization"] = current_org.id

        ser = self.serializer_class(data=data)
        ser.is_valid(raise_exception=True)

        new_user = User.objects.create(email=data["email"])
        new_user.set_password(data["password"])
        new_user.save()

        user_data = self.serializer_class(new_user)

        data["organization"] = Organization.objects.get(id=current_org.id)
        EmployeeInformation.objects.update_or_create(
            user=new_user,
            defaults={
                "user": new_user,
                **data,
            },
        )
        return response.Response(user_data.data)
