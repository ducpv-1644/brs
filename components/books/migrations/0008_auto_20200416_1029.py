# Generated by Django 3.0.5 on 2020-04-16 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20200416_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrequestbuy',
            name='book_url',
            field=models.URLField(max_length=512),
        ),
    ]
