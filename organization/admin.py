from django.contrib import admin
from .models import Organization, Device, DevicedDelegate

admin.site.register(Organization)
admin.site.register(Device)
admin.site.register(DevicedDelegate)
