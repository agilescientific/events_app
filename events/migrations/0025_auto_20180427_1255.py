# Generated by Django 2.0.2 on 2018-04-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20180426_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='sponsors',
            field=models.ManyToManyField(blank=True, to='events.Organization'),
        ),
    ]
