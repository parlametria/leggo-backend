# Generated by Django 2.1.2 on 2018-10-19 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20181017_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='progresso',
            name='pulou',
            field=models.NullBooleanField(help_text='TRUE se a proposicao pulou a fase, FALSE caso contrario'),
        ),
    ]