# Generated by Django 2.1 on 2018-09-05 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180905_1154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposicao',
            options={'ordering': ('-data_apresentacao',)},
        ),
        migrations.AlterModelOptions(
            name='tramitacaoevent',
            options={'ordering': ('sequencia',)},
        ),
    ]
