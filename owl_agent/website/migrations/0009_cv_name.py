# Generated by Django 3.1.7 on 2021-04-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20210418_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
