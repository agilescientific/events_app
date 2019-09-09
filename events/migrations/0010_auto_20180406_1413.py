# Generated by Django 2.0.2 on 2018-04-06 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20180306_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventclass',
            options={'verbose_name_plural': 'Event Classes'},
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_info', to='events.Event'),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='detail_long',
            field=models.TextField(default='', max_length=1000, verbose_name='Long Description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='detail_small',
            field=models.TextField(default='', max_length=500, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='github',
            field=models.URLField(verbose_name='URL to Github Repo'),
        ),
    ]
