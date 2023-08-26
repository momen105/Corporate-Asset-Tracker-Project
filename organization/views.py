from .serializers import (
    CreateOrganizationSerializer,
    DeviceSerializer,
    DeviceDelegateSerializer,
    DeviceReceivedSerializer,
)
from users.apipermissions import IsOwner, IsOrganizationAdmin
from rest_framework import generics, response, permissions, exceptions
from .models import Organization, Device, DeviceDelegate, DeviceReceived
from django.shortcuts import get_object_or_404


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


class DeviceReceivedView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceReceivedSerializer
    queryset = DeviceReceived.objects.all()

    def get(self, request, *args, **kwargs):
        current_org = self.request.user.employee_information_user.organization
        if received_id := self.kwargs.get("id"):
            result = get_object_or_404(
                DeviceReceived,
                id=received_id,
                delegated_device__device__organization=current_org,
            )
            ser = self.serializer_class(result)
        else:
            result = self.queryset.filter(
                delegated_device__device__organization=current_org
            )
            ser = self.serializer_class(result, many=True)

        return response.Response(ser.data)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        current_user = self.request.user

        if data.get("delegated_device") != current_user.id:
            raise exceptions.PermissionDenied("You can't receive this device")

        ser = self.serializer_class(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return response.Response(ser.data)


class DeviceReturnView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceReceivedSerializer
    queryset = DeviceReceived.objects.all()

    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = self.request.data
        if data.get("return_date") and data.get("device_return_condition"):
            ser = self.get_serializer(instance, data=data, partial=partial)
            ser.is_valid(raise_exception=True)
            self.perform_update(ser)
        else:
            raise exceptions.NotAcceptable(
                "Please given the return date and device condition"
            )

        return super().update(request, *args, **kwargs)
