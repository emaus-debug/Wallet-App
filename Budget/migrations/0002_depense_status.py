# Generated by Django 4.0.3 on 2022-03-24 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='depense',
            name='status',
            field=models.CharField(choices=[('ACTIF', 'Freshman'), ('ACHEVE', 'Sophomore')], default='ACTIF', max_length=6),
        ),
    ]
