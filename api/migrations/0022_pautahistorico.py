# Generated by Django 2.1.3 on 2018-11-22 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20181119_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='PautaHistorico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='data')),
                ('local', models.TextField(blank=True)),
                ('em_pauta', models.NullBooleanField(help_text='TRUE se a proposicao estiver em pauta, FALSE caso contrario')),
                ('proposicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pauta_historico', to='api.EtapaProposicao')),
            ],
            options={
                'ordering': ('-data',),
                'get_latest_by': '-data',
            },
        ),
    ]
