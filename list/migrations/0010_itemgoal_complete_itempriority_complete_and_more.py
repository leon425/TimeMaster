# Generated by Django 4.0.4 on 2023-08-12 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0009_timebox_weeknum'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemgoal',
            name='complete',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='itempriority',
            name='complete',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='itemschedule',
            name='complete',
            field=models.BooleanField(null=True),
        ),
    ]