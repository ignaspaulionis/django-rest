# Generated by Django 2.2.1 on 2019-05-15 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190514_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time_minutes',
            field=models.IntegerField(),
        ),
    ]
