# Generated by Django 2.0.2 on 2018-04-24 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_project_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_time',
        ),
        migrations.AddField(
            model_name='event',
            name='event_enddate',
            field=models.DateTimeField(null=True, verbose_name='event end'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_startdate',
            field=models.DateField(null=True, verbose_name='event start'),
        ),
    ]