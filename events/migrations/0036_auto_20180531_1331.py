# Generated by Django 2.0.2 on 2018-05-31 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_remove_event_sponsors'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sponsors',
            field=models.ManyToManyField(blank=True, related_name='sponsor_list', to='events.EventSponsorship'),
        ),
        migrations.AlterField(
            model_name='event',
            name='slack_webhook',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]