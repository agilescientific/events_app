# Generated by Django 2.0.2 on 2018-08-08 21:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0042_idea_detail_short'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideacomment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
