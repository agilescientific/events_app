# Generated by Django 2.0.2 on 2018-08-07 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0039_ideacomment_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='need_ideas',
            field=models.NullBooleanField(),
        ),
    ]
