# Generated by Django 5.1.4 on 2024-12-31 17:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_offreemploi_date_limite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offreemploi',
            name='date_limite',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 30, 18, 32, 13, 921240)),
        ),
    ]
