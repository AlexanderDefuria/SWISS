# Generated by Django 2.2.13 on 2021-05-18 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0040_auto_20210518_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='pick_status',
            field=models.IntegerField(default=0),
        ),
    ]
