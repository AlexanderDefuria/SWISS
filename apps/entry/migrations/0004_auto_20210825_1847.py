# Generated by Django 2.2.13 on 2021-08-25 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0003_team_reg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='reg_id',
            field=models.CharField(default='team', max_length=50),
        ),
    ]
