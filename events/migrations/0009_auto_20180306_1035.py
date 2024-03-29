# Generated by Django 2.0.2 on 2018-03-06 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_auto_20180302_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_class', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('detail_small', models.TextField(default='', max_length=200)),
                ('detail_long', models.TextField(default='', max_length=500)),
                ('votes', models.BigIntegerField(default=0)),
                ('github', models.URLField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectCreator', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.EventClass'),
            preserve_default=False,
        ),
    ]
