# Generated by Django 3.2.9 on 2021-12-09 08:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=225)),
                ('customer_name', models.CharField(max_length=225)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=225)),
                ('location', models.CharField(max_length=225)),
                ('customer_added_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=225)),
                ('description', models.CharField(max_length=225)),
                ('step_document', models.FileField(upload_to='documents')),
                ('notarize', models.CharField(max_length=10)),
                ('apostille', models.CharField(max_length=10)),
                ('file_add_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=225)),
                ('internal_note', models.TextField()),
                ('lead', models.CharField(max_length=12)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(max_length=225)),
                ('customerName', models.CharField(max_length=225)),
                ('description', models.TextField()),
                ('userFile', models.FileField(upload_to='userfiles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=225, null=True)),
                ('city', models.CharField(blank=True, max_length=225, null=True)),
                ('profilepic', models.ImageField(default='media/profilepic.png', upload_to='media')),
                ('address', models.TextField(blank=True, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=225, null=True)),
                ('userrelation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Steps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('description', models.CharField(max_length=224)),
                ('instruction', models.TextField()),
                ('visibility', models.CharField(max_length=20)),
                ('download', models.CharField(max_length=20)),
                ('upload', models.CharField(max_length=20)),
                ('file', models.FileField(upload_to='stepfiles')),
                ('project_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_template', to='stepautomationapp.projecttemplate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=225)),
                ('countryrel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stepautomationapp.country')),
            ],
        ),
    ]
