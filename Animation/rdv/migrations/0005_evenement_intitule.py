# Generated by Django 3.2.5 on 2021-07-29 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdv', '0004_auto_20210728_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='intitule',
            field=models.CharField(max_length=500, null=True, verbose_name="Intitulé de l'événement"),
        ),
    ]