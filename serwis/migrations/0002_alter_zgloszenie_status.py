# Generated by Django 3.2.8 on 2021-11-07 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serwis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zgloszenie',
            name='status',
            field=models.IntegerField(choices=[(2, 'Otwarty'), (3, 'Czeka na wyjaśnienie'), (5, 'Anulowany'), (1, 'Nowy'), (4, 'Zamknięty')], default=1),
        ),
    ]
