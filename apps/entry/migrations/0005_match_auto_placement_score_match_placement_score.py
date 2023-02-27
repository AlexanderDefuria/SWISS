# Generated by Django 4.0.9 on 2023-02-18 18:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0004_pointsconfig_alter_match_auto_placement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='auto_placement_score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='match',
            name='placement_score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(0)]),
        ),
    ]
