from django.contrib.auth.password_validation import validate_password
from .models import User, EmployeeInformation
from rest_framework import serializers, response, status
from organization.models import Organization


class EmployeeInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeInformation
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    # This password could have been automated and the employee could have been emailed with his password
    # which would have made the project even better. But on this project,
    # this is not the main work.so i skipped this work. but, I can do this.

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    organization = serializers.PrimaryKeyRelatedField(
        source="employee_information_user.organization",
        queryset=Organization.objects.all(),
        required=True,
        write_only=True,
    )
    first_name = serializers.CharField(
        source="employee_information_user.first_name",
        required=False,
    )
    last_name = serializers.CharField(
        source="employee_information_user.last_name",
        required=False,
    )
    nid_number = serializers.CharField(
        source="employee_information_user.nid_number",
        required=False,
    )
    religion = serializers.CharField(
        source="employee_information_user.religion",
        required=False,
    )
    birth_date = serializers.CharField(
        source="employee_information_user.birth_date",
        required=False,
    )
    gender = serializers.CharField(
        source="employee_information_user.gender",
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "organization",
            "first_name",
            "last_name",
            "nid_number",
            "religion",
            "birth_date",
            "gender",
        )
        read_only_fields = ("id",)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create(email=validated_data["email"], is_staff=True)
        user.set_password(validated_data["password"])
        user.save()

        if employee_information_user := validated_data.get("employee_information_user"):
            EmployeeInformation.objects.update_or_create(
                user=user, defaults={"user": user, **employee_information_user}
            )
        return user
