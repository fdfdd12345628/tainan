# Generated by Django 2.2.6 on 2019-10-29 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='hole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('town', models.CharField(max_length=5)),
                ('positionLon', models.FloatField()),
                ('positionLat', models.FloatField()),
                ('occurTime', models.DateTimeField()),
                ('reason', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('flood', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('temperature', models.FloatField()),
                ('highestTemperature', models.FloatField()),
                ('lowestTemperature', models.FloatField()),
                ('dewPointTemperature', models.FloatField()),
                ('minDewPointTemperature', models.FloatField()),
                ('relativeHumidity', models.FloatField()),
                ('rainfall', models.FloatField()),
                ('maxTenMinuteRainFall', models.FloatField()),
                ('maxSixtyMinuteRainFall', models.FloatField()),
            ],
        ),
    ]
