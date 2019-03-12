# Generated by Django 2.0.2 on 2018-05-31 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_auto_20180516_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSponsorship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=20, null=True)),
                ('tier', models.CharField(max_length=100, null=True)),
                ('size', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='slack_webhook',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='eventsponsorship',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_esponsored', to='events.Event'),
        ),
        migrations.AddField(
            model_name='eventsponsorship',
            name='sponsor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsor_info', to='events.Organization'),
        ),
    ]
