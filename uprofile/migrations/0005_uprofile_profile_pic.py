# Generated by Django 2.0.2 on 2018-04-10 02:38

from django.db import migrations, models
import uprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('uprofile', '0004_auto_20180406_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='uprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=uprofile.models.user_directory_path),
        ),
    ]
