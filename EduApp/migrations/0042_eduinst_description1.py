# Generated by Django 5.0.7 on 2024-11-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0041_eduinst_website_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="eduinst",
            name="Description1",
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]