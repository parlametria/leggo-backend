# Generated by Django 3.0 on 2019-12-04 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0071_merge_20191204_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapaproposicao',
            name='advocacy_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proposicao',
            name='advocacy_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
