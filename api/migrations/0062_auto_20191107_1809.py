# Generated by Django 2.2.6 on 2019-11-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_auto_20191105_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atores',
            name='qtd_de_documentos',
        ),
        migrations.AddField(
            model_name='atores',
            name='peso_total_documentos',
            field=models.FloatField(default=0, verbose_name='Quantidade de documentos feitas por um determinado autor'),
            preserve_default=False,
        ),
    ]