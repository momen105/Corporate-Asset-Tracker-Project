from django.db import models
from core.models import BaseModel


class Organization(BaseModel):
    """
    Model to store organization data
    """

    name = models.CharField(max_length=255)
    address_two = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    email = models.EmailField()
    trade_license = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class Device(BaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    in_stock = models.IntegerField(default=0)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="organization_device"
    )

    def __str__(self):
        return f"{self.id} | {self.name}"

    class Meta:
        ordering = ["-id"]


class DevicedDelegate(BaseModel):
    employee = models.ForeignKey(
        "users.user", on_delete=models.CASCADE, related_name="employee_delegated_device"
    )
    device = models.ManyToManyField(Device, related_name="delegated_devices")
    device_condition = models.TextField()
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} | {self.employee.email}"

    class Meta:
        ordering = ["-id"]
