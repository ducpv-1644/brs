# Generated by Django 3.0.5 on 2020-04-20 11:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_auto_20200420_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='messages',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=512), size=5), size=None),
        ),
    ]
