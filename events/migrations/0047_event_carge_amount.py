# Generated by Django 2.0.2 on 2019-01-11 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('events', '0046_auto_20181014_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='carge_amount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_amount_info', to='payments.Amount'),
        ),
    ]
