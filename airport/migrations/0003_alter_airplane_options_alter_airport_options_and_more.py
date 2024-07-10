# Generated by Django 5.0.6 on 2024-07-01 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="airplane",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="airport",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="flight",
            options={"ordering": ["-departure_time"]},
        ),
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["row", "seat"]},
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("flight", "row", "seat")},
        ),
    ]
