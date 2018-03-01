# Generated by Django 2.0.2 on 2018-02-27 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_auto_20180226_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('leader', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teamleader', to=settings.AUTH_USER_MODEL)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]