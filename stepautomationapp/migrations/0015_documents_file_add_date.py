# Generated by Django 3.2.8 on 2021-11-23 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stepautomationapp', '0014_alter_documents_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='file_add_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
