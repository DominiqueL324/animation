# Generated by Django 3.2.5 on 2021-08-06 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdv', '0007_auto_20210803_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='code',
            field=models.CharField(max_length=10, null=True, verbose_name='Code du rendez-vous'),
        ),
    ]
