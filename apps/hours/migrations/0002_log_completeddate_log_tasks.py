# Generated by Django 4.0.1 on 2022-01-22 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='completedDate',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='log',
            name='tasks',
            field=models.TextField(default=''),
        ),
    ]