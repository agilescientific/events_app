# Generated by Django 2.0.2 on 2018-05-31 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_auto_20180531_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='sponsors',
        ),
    ]
