# Generated by Django 2.0.2 on 2018-04-19 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_project_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=140, null=True),
        ),
    ]
