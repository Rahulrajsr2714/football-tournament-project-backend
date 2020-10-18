# Generated by Django 2.2.13 on 2020-10-17 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('footballapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMatches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('team_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teama', to='footballapp.TeamDetails')),
                ('team_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamb', to='footballapp.TeamDetails')),
            ],
        ),
    ]
