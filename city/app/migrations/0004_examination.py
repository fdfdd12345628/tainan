# Generated by Django 2.2.6 on 2019-12-12 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20191029_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='examination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positionLon', models.FloatField()),
                ('positionLat', models.FloatField()),
                ('examinationTime', models.DateTimeField()),
                ('photoURL', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
