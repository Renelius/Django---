# Generated by Django 3.0 on 2020-04-21 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_bd_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bd',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Изображение'),
        ),
    ]
