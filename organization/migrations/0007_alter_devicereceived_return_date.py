# Generated by Django 4.2.4 on 2023-08-26 08:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0006_alter_devicereceived_device_return_condition_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devicereceived",
            name="return_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
