# Generated by Django 2.0.2 on 2018-04-24 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uprofile', '0006_auto_20180410_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='uprofile',
            name='linkedin_uname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='uprofile',
            name='twitter_uname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
