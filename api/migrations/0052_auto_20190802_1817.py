# Generated by Django 2.2.3 on 2019-08-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_atores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atores',
            name='id_autor',
            field=models.FloatField(verbose_name='Id do autor do documento'),
        ),
    ]