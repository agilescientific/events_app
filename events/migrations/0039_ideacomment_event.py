# Generated by Django 2.0.2 on 2018-08-07 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_remove_ideacomment_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideacomment',
            name='event',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='commentEvent', to='events.Event'),
            preserve_default=False,
        ),
    ]