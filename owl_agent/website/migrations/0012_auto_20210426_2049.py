# Generated by Django 3.1.4 on 2021-04-26 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20210421_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_offer',
            name='location',
            field=models.CharField(choices=[('İstanbul', 'Istanbul'), ('Ankara', 'Ankara'), ('İzmir', 'Izmir'), ('Bursa', 'Bursa')], max_length=500),
        ),
    ]