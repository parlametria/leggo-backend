# Generated by Django 3.0.7 on 2020-10-13 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0098_auto_20201005_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapaproposicao',
            name='status',
            field=models.TextField(blank=True, null=True),
        ),
    ]
