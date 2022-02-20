# Generated by Django 4.0.1 on 2022-02-12 20:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0015_alter_teammember_position_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='auto_start_x',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='match',
            name='auto_start_y',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='match',
            name='defense_played',
            field=models.BooleanField(default=False),
        ),
    ]
