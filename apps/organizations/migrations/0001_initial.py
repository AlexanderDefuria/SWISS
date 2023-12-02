# Generated by Django 4.1.7 on 2023-12-01 22:51

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='NA')),
                ('FIRST_key', models.TextField(default='NA')),
                ('FIRST_district_key', models.TextField(default='NA')),
                ('FIRST_eventType', models.TextField(default='NA')),
                ('start', models.DateField(default=datetime.date(2020, 1, 1), validators=[django.core.validators.MaxValueValidator(datetime.date(2220, 12, 31)), django.core.validators.MinValueValidator(datetime.date(2020, 1, 1))])),
                ('end', models.DateField(default=datetime.date(2020, 1, 1), validators=[django.core.validators.MaxValueValidator(datetime.date(2220, 12, 31)), django.core.validators.MinValueValidator(datetime.date(2020, 1, 1))])),
                ('imported', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('reg_id', models.UUIDField(default=uuid.uuid4)),
            ],
            options={
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='OrgSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_photos', models.BooleanField(default=True)),
                ('allow_schedule', models.BooleanField(default=True)),
                ('new_user_creation', models.CharField(choices=[('MA', 'Manual Approval, Open Registration'), ('MM', 'Manual Creation of All Users'), ('AA', 'Open Registration and Use')], default='MM', max_length=2)),
                ('new_user_position', models.CharField(choices=[('PA', 'Public Access'), ('OV', 'Only View'), ('MS', 'Match Scout'), ('PS', 'Pit Scout'), ('GS', 'General Scout'), ('DT', 'Drive Team'), ('LS', 'Lead Scout')], default='OV', max_length=2)),
                ('current_event', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='organizations.event')),
            ],
            options={
                'verbose_name_plural': 'Organization Settings',
            },
        ),
        migrations.CreateModel(
            name='OrgMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutorial_completed', models.BooleanField(default=False)),
                ('position', models.CharField(choices=[('PA', 'Public Access'), ('OV', 'Only View'), ('MS', 'Match Scout'), ('PS', 'Pit Scout'), ('GS', 'General Scout'), ('DT', 'Drive Team'), ('LS', 'Lead Scout'), ('NA', 'No Access')], default='GS', max_length=2)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='settings',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='organizations.orgsettings'),
        ),
    ]
