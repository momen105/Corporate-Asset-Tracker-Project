# Generated by Django 4.2.4 on 2023-08-26 08:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0005_devicereceived"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devicereceived",
            name="device_return_condition",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="devicereceived",
            name="return_date",
            field=models.DateTimeField(blank=True),
        ),
    ]
