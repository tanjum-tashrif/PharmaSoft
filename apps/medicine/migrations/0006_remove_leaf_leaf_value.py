# Generated by Django 5.1.3 on 2025-01-01 04:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("medicine", "0005_leaf_leaf_value_unit_unit_value"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leaf",
            name="leaf_value",
        ),
    ]
