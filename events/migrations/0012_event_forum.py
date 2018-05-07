# Generated by Django 2.0.2 on 2018-04-10 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20170928_2327'),
        ('events', '0011_project_main_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='forum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_forum', to='forum.Forum'),
        ),
    ]
