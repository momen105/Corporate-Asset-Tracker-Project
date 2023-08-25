from .serializers import CreateOrganizationSerializer
from users.apipermissions import IsOwner
from rest_framework import generics, response
from .models import Organization


class OrganizationView(
    generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsOwner]
    serializer_class = CreateOrganizationSerializer
    queryset = Organization.objects.all()

    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if org_id := self.kwargs.get("org_id"):
            org = self.queryset.get(id=org_id)
            ser = self.serializer_class(org)
        else:
            org = self.queryset.all()
            ser = self.serializer_class(org, many=True)

        return response.Response(ser.data)
