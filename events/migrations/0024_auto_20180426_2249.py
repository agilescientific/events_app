# Generated by Django 2.0.2 on 2018-04-27 01:49

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20180426_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='logo_inline_url',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='logo_url',
        ),
        migrations.AddField(
            model_name='event',
            name='banner_img',
            field=models.ImageField(blank=True, default='http://placehold.it/1000x300', null=True, upload_to=events.models.logo_directory_path),
        ),
    ]
