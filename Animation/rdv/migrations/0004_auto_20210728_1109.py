# Generated by Django 3.2.5 on 2021-07-28 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rdv', '0003_auto_20210727_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rendezvous',
            old_name='client',
            new_name='administre',
        ),
        migrations.RenameField(
            model_name='rendezvous',
            old_name='date_r',
            new_name='date_d',
        ),
        migrations.RenameField(
            model_name='rendezvous',
            old_name='heure_r',
            new_name='heure_d',
        ),
    ]
