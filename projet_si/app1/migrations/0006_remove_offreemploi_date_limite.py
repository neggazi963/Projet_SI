# Generated by Django 5.1.4 on 2024-12-31 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_offreemploi_date_limite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offreemploi',
            name='date_limite',
        ),
    ]
