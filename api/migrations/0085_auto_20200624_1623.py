# Generated by Django 3.0.7 on 2020-06-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_anotacaogeral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anotacaogeral',
            name='interesse',
            field=models.TextField(help_text='Interesse da Proposição'),
        ),
    ]
