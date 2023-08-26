from .models import Organization, Device
from rest_framework import serializers


class CreateOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(DeviceSerializer, self).to_representation(instance)
        representation["organization"] = CreateOrganizationSerializer(
            instance.organization
        ).data.get("name")

        return representation
