# Generated by Django 4.2.1 on 2023-08-27 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_offre', models.IntegerField(default=0)),
                ('count_demande', models.IntegerField(default=0)),
                ('supervisor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supervisor',
            },
        ),
        migrations.CreateModel(
            name='Stagiaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_Name', models.CharField(max_length=255)),
                ('fisrt_Name', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('motivation', models.TextField()),
                ('niveau', models.CharField(max_length=50)),
                ('image', models.ImageField(default='photos/default.jpg', upload_to='photos/')),
                ('cv', models.FileField(upload_to='pdfs/')),
                ('status', models.IntegerField(default=0)),
                ('stagiaire_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'stagiaire',
            },
        ),
        migrations.CreateModel(
            name='Offre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('domaine', models.CharField(max_length=255)),
                ('mission', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('skills_needed', models.CharField(max_length=255)),
                ('dure', models.CharField(max_length=255)),
                ('niveau_etude', models.CharField(max_length=255)),
                ('count', models.IntegerField()),
                ('valable', models.IntegerField(default=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stagiaire.supervisor')),
            ],
            options={
                'db_table': 'offre',
            },
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.IntegerField(default=0)),
                ('offre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stagiaire.offre')),
                ('owner_stagiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stagiaire.stagiaire')),
            ],
            options={
                'db_table': 'demande',
            },
        ),
    ]
