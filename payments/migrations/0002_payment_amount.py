# Generated by Django 2.0.2 on 2019-01-11 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.Amount'),
        ),
    ]
