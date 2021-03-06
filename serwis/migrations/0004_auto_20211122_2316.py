# Generated by Django 3.2.9 on 2021-11-22 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serwis', '0003_auto_20211107_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='zgloszenie',
            name='czas_wykonania',
            field=models.TimeField(blank=True, default='00:00', null=True, verbose_name='czas wykonania'),
        ),
        migrations.AddField(
            model_name='zgloszenie',
            name='data_wykonania',
            field=models.DateField(blank=True, default='1900-01-01', null=True, verbose_name='data wykonania'),
        ),
        migrations.AlterField(
            model_name='zgloszenie',
            name='status',
            field=models.IntegerField(choices=[(3, 'Czeka na wyjaśnienie'), (1, 'Nowy'), (5, 'Zamknięty'), (4, 'Wykonany'), (6, 'Anulowany'), (2, 'Otwarty')], default=1),
        ),
    ]
