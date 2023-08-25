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
