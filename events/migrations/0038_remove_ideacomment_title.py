# Generated by Django 2.0.2 on 2018-08-07 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0037_auto_20180731_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ideacomment',
            name='title',
        ),
    ]
