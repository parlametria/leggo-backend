# Generated by Django 2.1.1 on 2018-09-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20180925_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='energiarecenteperiodo',
            name='casa',
        ),
        migrations.RemoveField(
            model_name='energiarecenteperiodo',
            name='id_ext',
        ),
        migrations.AlterField(
            model_name='energiarecenteperiodo',
            name='periodo',
            field=models.DateField(verbose_name='periodo'),
        ),
    ]