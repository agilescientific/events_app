# Generated by Django 2.0.2 on 2019-01-14 23:39

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0049_auto_20190111_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='rules',
            field=markdownx.models.MarkdownxField(blank=True, default='', max_length=10000, null=True),
        ),
    ]
