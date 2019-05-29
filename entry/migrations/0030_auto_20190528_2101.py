# Generated by Django 2.2 on 2019-05-28 21:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0029_event_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100000000), django.core.validators.MinValueValidator(0)]),
        ),
    ]
