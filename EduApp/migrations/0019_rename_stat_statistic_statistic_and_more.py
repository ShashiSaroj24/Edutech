# Generated by Django 5.0.7 on 2024-09-05 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0018_rename_statistics_statistic_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="statistic",
            old_name="Stat",
            new_name="Statistic",
        ),
        migrations.RenameField(
            model_name="statistic_detail",
            old_name="Stat",
            new_name="Statistic",
        ),
    ]
