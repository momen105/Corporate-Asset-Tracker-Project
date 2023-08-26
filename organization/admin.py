from django.contrib import admin
from .models import Organization, Device, DeviceDelegate

admin.site.register(Organization)
admin.site.register(Device)
admin.site.register(DeviceDelegate)
