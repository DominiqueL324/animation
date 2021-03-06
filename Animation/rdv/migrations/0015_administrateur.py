# Generated by Django 3.2.5 on 2021-08-11 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rdv', '0014_rename_respnsable_service_responsable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=300, null=True, verbose_name='Adresse')),
                ('telephone', models.IntegerField(null=True, verbose_name='Téléphone')),
                ('password', models.CharField(default='password', max_length=300, verbose_name='Mot de passe')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='administrateur', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'administrateur',
            },
        ),
    ]
