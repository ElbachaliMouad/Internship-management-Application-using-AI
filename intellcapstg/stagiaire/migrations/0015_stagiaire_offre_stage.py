# Generated by Django 4.2.1 on 2023-09-13 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stagiaire', '0014_alter_stagiaire_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='stagiaire',
            name='offre_stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stagiaire.offre'),
        ),
    ]
