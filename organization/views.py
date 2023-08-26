from .serializers import (
    CreateOrganizationSerializer,
    DeviceSerializer,
    DeviceDelegateSerializer,
)
from users.apipermissions import IsOwner, IsOrganizationAdmin
from rest_framework import generics, response, permissions
from .models import Organization, Device, DeviceDelegate


class OrganizationView(
    generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsOwner]
    serializer_class = CreateOrganizationSerializer
    queryset = Organization.objects.all()

    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if org_id := self.kwargs.get("id"):
            org = self.queryset.get(id=org_id)
            ser = self.serializer_class(org)
        else:
            org = self.queryset.all()
            ser = self.serializer_class(org, many=True)

        return response.Response(ser.data)


class DeviceView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner, IsOrganizationAdmin]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if device_id := self.kwargs.get("id"):
            device = self.queryset.get(id=device_id)
            ser = self.serializer_class(device)
        else:
            device = self.queryset.all()
            ser = self.serializer_class(device, many=True)

        return response.Response(ser.data)

    def create(self, request, *args, **kwargs):
        current_user_org = self.request.user.employee_information_user.organization
        data = self.request.data
        data["organization"] = current_user_org.id
        ser = self.serializer_class(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return response.Response(ser.data)


class DeviceDelegateView(
    generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsOwner, IsOrganizationAdmin]
    serializer_class = DeviceDelegateSerializer
    queryset = DeviceDelegate.objects.all()

    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method in ["POST", "PATCH", "PUT"]:
            self.permission_classes = [IsOwner, IsOrganizationAdmin]
        return super(DeviceDelegateView, self).get_permissions()

    def get(self, request, *args, **kwargs):
        current_org = self.request.user.employee_information_user.organization
        if delegate_id := self.kwargs.get("id"):
            delegated_device = self.queryset.filter(
                id=delegate_id, device__organization=current_org
            ).first()
            ser = self.serializer_class(delegated_device)
        else:
            delegated_device = self.queryset.filter(
                device__organization=current_org,
            )
            ser = self.serializer_class(delegated_device, many=True)

        return response.Response(ser.data)
