# Generated by Django 2.2.1 on 2019-05-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramitador', '0006_auto_20190528_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents/%Y/%m/%d/'),
        ),
    ]
