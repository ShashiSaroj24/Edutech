# Generated by Django 5.0.7 on 2024-08-07 12:36

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0002_contact_model_msg"),
    ]

    operations = [
        migrations.CreateModel(
            name="Register_model",
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
                ("Name", models.CharField(max_length=10000)),
                ("Email", models.CharField(max_length=10000)),
                ("Password", ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.RenameField(
            model_name="contact_model",
            old_name="email",
            new_name="Email",
        ),
        migrations.RenameField(
            model_name="contact_model",
            old_name="msg",
            new_name="Msg",
        ),
    ]