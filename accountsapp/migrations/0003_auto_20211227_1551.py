# Generated by Django 3.2.9 on 2021-12-27 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountsapp', '0002_rename_userrelation_guideeproflie_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guideeproflie',
            name='address',
        ),
        migrations.RemoveField(
            model_name='guideeproflie',
            name='city',
        ),
        migrations.RemoveField(
            model_name='guideeproflie',
            name='country',
        ),
        migrations.RemoveField(
            model_name='guideeproflie',
            name='profilepic',
        ),
        migrations.RemoveField(
            model_name='guideeproflie',
            name='zipcode',
        ),
    ]
