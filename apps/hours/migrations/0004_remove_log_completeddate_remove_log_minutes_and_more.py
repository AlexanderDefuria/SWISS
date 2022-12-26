# Generated by Django 4.0.6 on 2022-08-10 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0003_alter_log_mentor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='completedDate',
        ),
        migrations.RemoveField(
            model_name='log',
            name='minutes',
        ),
        migrations.AlterField(
            model_name='log',
            name='tasks',
            field=models.TextField(default='', null=True),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hours.gremlin')),
            ],
        ),
    ]