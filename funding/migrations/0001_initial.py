# Generated by Django 4.2.3 on 2023-08-06 14:00

import datetime
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
            name='Funding',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField(max_length=255)),
                ('goal_amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(10000000)])),
                ('current_amount', models.IntegerField(default=0)),
                ('expire_on', models.DateTimeField(default=datetime.datetime(2023, 9, 5, 14, 0, 38, 72761, tzinfo=datetime.timezone.utc))),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('public', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='funding_image/')),
                ('is_transmitted', models.BooleanField(default=False)),
                ('review', models.TextField(null=True)),
                ('review_image', models.ImageField(null=True, upload_to='review_image/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Funding', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
