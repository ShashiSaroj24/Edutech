# Generated by Django 5.0.7 on 2024-08-16 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0004_alter_register_model_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="register_model",
            name="PhoneNo",
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name="register_model",
            name="Pincode",
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]