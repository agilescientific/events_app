# Generated by Django 2.0.2 on 2018-08-08 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0041_auto_20180807_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='detail_short',
            field=models.CharField(default='', max_length=200, verbose_name='Short description'),
        ),
    ]
