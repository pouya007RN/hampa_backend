# Generated by Django 3.0.2 on 2020-04-22 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200420_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='name',
        ),
    ]