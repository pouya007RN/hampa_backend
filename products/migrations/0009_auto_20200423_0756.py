# Generated by Django 3.0.2 on 2020-04-23 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20200422_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]