# Generated by Django 2.1.3 on 2019-04-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20190412_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='emendas',
            name='tipo_documento',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
