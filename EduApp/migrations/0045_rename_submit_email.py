# Generated by Django 5.0.7 on 2024-11-13 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0044_submit"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Submit",
            new_name="Email",
        ),
    ]