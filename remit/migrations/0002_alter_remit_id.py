# Generated by Django 4.2.3 on 2023-07-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remit',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
