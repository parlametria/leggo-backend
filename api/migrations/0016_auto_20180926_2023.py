# Generated by Django 2.1.1 on 2018-09-26 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20180926_1950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='energiahistorico',
            options={'ordering': ('-periodo',)},
        ),
    ]