# Generated by Django 2.0.2 on 2019-01-11 18:28

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='amount',
            name='long_description',
            field=markdownx.models.MarkdownxField(default='', max_length=1000, verbose_name='Elaborate description (payment)'),
        ),
        migrations.AlterField(
            model_name='amount',
            name='currency',
            field=models.CharField(max_length=20, verbose_name='Currency (3 char)'),
        ),
    ]
