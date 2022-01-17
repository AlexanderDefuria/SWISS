# Generated by Django 4.0.1 on 2022-01-10 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0004_alter_team_glance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start']},
        ),
        migrations.AlterModelOptions(
            name='images',
            options={'ordering': ['name'], 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-match_number'], 'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterModelOptions(
            name='pits',
            options={'ordering': ['team'], 'verbose_name_plural': 'Pits'},
        ),
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['match_number'], 'verbose_name_plural': 'Schedule'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['number']},
        ),
        migrations.AlterModelOptions(
            name='teamsettings',
            options={'verbose_name_plural': 'Team Settings'},
        ),
        migrations.AddField(
            model_name='event',
            name='FIRST_district_key',
            field=models.TextField(default='NA'),
        ),
    ]