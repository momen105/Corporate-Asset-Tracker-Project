from django.contrib import admin
from .models import Organization, Device, DeviceDelegate, DeviceReceived

admin.site.register(Organization)
admin.site.register(Device)
admin.site.register(DeviceDelegate)
admin.site.register(DeviceReceived)
