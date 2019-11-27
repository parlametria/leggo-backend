# Generated by Django 2.2.6 on 2019-11-25 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_merge_20191119_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoria',
            name='casa',
            field=models.TextField(default='', help_text='Casa.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='autoria',
            name='id_principal',
            field=models.IntegerField(default=0, help_text='Id da proposição.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='autoria',
            name='sigla_local',
            field=models.TextField(default='', help_text='Sigla do local do documento.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coautoriaedge',
            name='casa',
            field=models.TextField(default='', help_text='Casa.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coautoriaedge',
            name='id_principal',
            field=models.IntegerField(default=0, help_text='Id da proposição.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coautoriaedge',
            name='sigla_local',
            field=models.TextField(default='', help_text='Sigla do local do documento.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coautorianode',
            name='casa',
            field=models.TextField(default='', help_text='Casa.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coautorianode',
            name='id_principal',
            field=models.IntegerField(default=0, help_text='Id da proposição.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coautorianode',
            name='sigla_local',
            field=models.TextField(default='', help_text='Sigla do local do documento.'),
            preserve_default=False,
        ),
    ]
