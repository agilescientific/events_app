# Generated by Django 2.0.2 on 2018-02-23 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20180222_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='img_url',
            field=models.CharField(default='http://placehold.it/700x300', max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(verbose_name='event date'),
        ),
    ]
