from .models import Organization, Device, DeviceDelegate, DeviceReceived
from rest_framework import serializers
from users.serializers import CreateUserSerializer


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


class DeviceDelegateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDelegate
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(DeviceDelegateSerializer, self).to_representation(
            instance
        )
        representation["device"] = DeviceSerializer(instance.device, many=True).data
        representation["employee"] = CreateUserSerializer(instance.employee).data

        return representation


class DeviceReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReceived
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(DeviceReceivedSerializer, self).to_representation(
            instance
        )

        representation["delegated_device"] = DeviceDelegateSerializer(
            instance.delegated_device
        ).data

        return representation
