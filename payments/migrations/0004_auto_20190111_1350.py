# Generated by Django 2.0.2 on 2019-01-11 18:50

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20190111_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='amount',
            name='img_url',
            field=models.URLField(default='https://placeimg.com/640/480/any', verbose_name='URL for payment image'),
        ),
        migrations.AlterField(
            model_name='amount',
            name='long_description',
            field=markdownx.models.MarkdownxField(default='', max_length=1000, verbose_name='Elaborate description (payment screen)'),
        ),
    ]
