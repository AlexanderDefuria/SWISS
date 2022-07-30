# Generated by Django 4.0.2 on 2022-03-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0019_schedule_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='position',
            field=models.CharField(choices=[('PA', 'Public Access'), ('OV', 'Only View'), ('MS', 'Match Scout'), ('PS', 'Pit Scout'), ('GS', 'General Scout'), ('DT', 'Drive Team'), ('LS', 'Lead Scout'), ('NA', 'No Access')], default='GS', max_length=2),
        ),
        migrations.AlterField(
            model_name='teamsettings',
            name='new_user_position',
            field=models.CharField(choices=[('PA', 'Public Access'), ('OV', 'Only View'), ('MS', 'Match Scout'), ('PS', 'Pit Scout'), ('GS', 'General Scout'), ('DT', 'Drive Team'), ('LS', 'Lead Scout')], default='OV', max_length=2),
        ),
    ]