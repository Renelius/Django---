# Generated by Django 3.0 on 2020-04-29 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0008_auto_20200424_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='bb',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='post',
            new_name='bb',
        ),
    ]
