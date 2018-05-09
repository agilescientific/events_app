# Generated by Django 2.0.2 on 2018-04-24 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20180424_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_location',
        ),
        migrations.AddField(
            model_name='event',
            name='event_location_address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_location_city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_location_country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_location_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]