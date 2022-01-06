# Generated by Django 3.2.5 on 2021-08-10 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rdv', '0010_service_respnsable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsable',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='utilisateur', to=settings.AUTH_USER_MODEL),
        ),
    ]
