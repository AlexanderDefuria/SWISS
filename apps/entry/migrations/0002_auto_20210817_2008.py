# Generated by Django 2.2.13 on 2021-08-17 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='team_ownership',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='entry.Team'),
        ),
        migrations.AddField(
            model_name='pits',
            name='team_ownership',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='entry.Team'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='team',
            field=models.ForeignKey(default=4343, on_delete=django.db.models.deletion.CASCADE, to='entry.Team'),
        ),
        migrations.AddField(
            model_name='teamsettings',
            name='team',
            field=models.ForeignKey(default=4343, on_delete=django.db.models.deletion.CASCADE, to='entry.Team'),
        ),
    ]
