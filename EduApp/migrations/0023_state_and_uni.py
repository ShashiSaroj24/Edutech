# Generated by Django 5.0.7 on 2024-09-09 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EduApp", "0022_delete_states"),
    ]

    operations = [
        migrations.CreateModel(
            name="State_and_Uni",
            fields=[
                (
                    "State_name",
                    models.CharField(
                        max_length=1000, primary_key=True, serialize=False
                    ),
                ),
                ("map_image", models.ImageField(upload_to="")),
            ],
        ),
    ]
