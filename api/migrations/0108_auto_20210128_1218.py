# Generated by Django 3.1.1 on 2021-01-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0107_auto_20210128_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destaques',
            name='data_aprovacao',
            field=models.DateField(blank=True, help_text='Data de finalização da proposição.', null=True),
        ),
        migrations.AlterField(
            model_name='destaques',
            name='data_req_urgencia_apresentado',
            field=models.DateField(blank=True, help_text='Data de de apresentação do requerimento de urgência.', null=True),
        ),
        migrations.AlterField(
            model_name='destaques',
            name='data_req_urgencia_aprovado',
            field=models.DateField(blank=True, help_text='Data de de aprovação do requerimento de urgência', null=True),
        ),
    ]
