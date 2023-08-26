# Generated by Django 4.2.4 on 2023-08-26 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organization", "0002_device"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="device",
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="DevicedDelegate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("device_condition", models.TextField()),
                ("from_date", models.DateTimeField()),
                ("to_date", models.DateTimeField()),
                (
                    "device",
                    models.ManyToManyField(
                        related_name="delegated_devices", to="organization.device"
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_delegated_device",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]