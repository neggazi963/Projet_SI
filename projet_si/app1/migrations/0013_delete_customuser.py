# Generated by Django 5.1.4 on 2025-01-11 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_alter_evaluation_options_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
