# Generated by Django 4.2.3 on 2023-08-06 14:00

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('bank_account', models.CharField(max_length=30, null=True)),
                ('birthday', models.CharField(max_length=4, null=True)),
                ('username', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=6)),
                ('age_range', models.CharField(max_length=5)),
                ('image', models.ImageField(null=True, upload_to='profile_image/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'account',
            },
            managers=[
                ('objects', account.models.FunSunUserManager()),
            ],
        ),
    ]
