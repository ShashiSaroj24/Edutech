# Generated by Django 5.0.7 on 2024-08-29 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0013_alter_register_model_profileimg"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "Name",
                    models.CharField(
                        max_length=1000, primary_key=True, serialize=False
                    ),
                ),
                ("Image", models.ImageField(blank=True, upload_to="data")),
            ],
        ),
    ]
