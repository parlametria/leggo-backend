# Generated by Django 2.1.1 on 2018-09-13 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_proposicao_apelido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposicao',
            name='apelido',
        ),
    ]
