# Generated by Django 5.0.7 on 2024-08-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0010_alter_college_phoneno_alter_universitie_phoneno"),
    ]

    operations = [
        migrations.AddField(
            model_name="register_model",
            name="Address",
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name="register_model",
            name="City",
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
