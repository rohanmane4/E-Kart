# Generated by Django 4.2 on 2023-05-29 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0009_alter_orderhistory_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]
