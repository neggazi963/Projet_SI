# Generated by Django 5.1.4 on 2024-12-26 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contrat',
            old_name='type_conge',
            new_name='type_contrat',
        ),
        migrations.RemoveField(
            model_name='conge',
            name='solde',
        ),
        migrations.RemoveField(
            model_name='contrat',
            name='jours_utilises',
        ),
        migrations.RemoveField(
            model_name='contrat',
            name='solde_initial',
        ),
        migrations.RemoveField(
            model_name='contrat',
            name='solde_restant',
        ),
        migrations.AddField(
            model_name='conge',
            name='jours_utilises',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conge',
            name='solde_initial',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conge',
            name='solde_restant',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contrat',
            name='salaire_mensuel',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='contrat',
            name='salaire_quotidien',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='conge',
            name='type_conge',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='date_fin',
            field=models.DateField(blank=True, null=True),
        ),
    ]
