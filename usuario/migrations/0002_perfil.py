# Generated by Django 3.2.13 on 2022-05-26 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('empresa', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='perfil', serialize=False, to='auth.user')),
            ],
        ),
    ]
