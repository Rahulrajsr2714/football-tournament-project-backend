# Generated by Django 2.2.13 on 2020-10-18 15:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('footballapp', '0003_auto_20201017_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammatches',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teammatches',
            name='date',
            field=models.DateField(),
        ),
    ]
