# Generated by Django 5.0.4 on 2024-05-11 11:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SWAG_basic", "0003_training_date_created_volunteer_date_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="training",
            name="gender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="SWAG_basic.gender",
            ),
        ),
    ]