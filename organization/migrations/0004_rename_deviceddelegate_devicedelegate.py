# Generated by Django 4.2.4 on 2023-08-26 07:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organization", "0003_alter_device_options_deviceddelegate"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DevicedDelegate",
            new_name="DeviceDelegate",
        ),
    ]
