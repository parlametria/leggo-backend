# Generated by Django 2.1.3 on 2018-11-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_pautahistorico_casa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pautahistorico',
            name='em_pauta',
            field=models.NullBooleanField(help_text='TRUE se a proposicao estiver em pauta, FALSE caso contrario'),
        ),
    ]
