# Generated by Django 2.2.6 on 2019-10-29 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_edges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodes',
            name='index',
        ),
    ]