# Generated by Django 4.0.6 on 2022-12-26 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0024_remove_match_balls_collected_alter_match_defended_by_and_more'),
    ]

    operations = [
        migrations.RenameModel('TeamMember', 'OrgMember'),
        migrations.RenameModel('TeamSettings', 'OrgSettings')
    ]