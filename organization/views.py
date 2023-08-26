from .serializers import CreateOrganizationSerializer, DeviceSerializer
from users.apipermissions import IsOwner, IsOrganizationAdmin
from rest_framework import generics, response
from .models import Organization, Device


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
