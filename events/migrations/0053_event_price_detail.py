# Generated by Django 2.0.2 on 2019-01-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0052_event_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price_detail',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
