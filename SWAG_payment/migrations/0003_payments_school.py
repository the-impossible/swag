# Generated by Django 5.0.4 on 2024-05-02 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SWAG_payment", "0002_states_schools"),
    ]

    operations = [
        migrations.AddField(
            model_name="payments",
            name="school",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="SWAG_payment.schools",
            ),
        ),
    ]
