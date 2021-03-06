# Generated by Django 3.1.4 on 2020-12-07 02:36

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("actor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="actor",
            name="id",
            field=models.UUIDField(
                db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="specie",
            name="id",
            field=models.UUIDField(
                db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
