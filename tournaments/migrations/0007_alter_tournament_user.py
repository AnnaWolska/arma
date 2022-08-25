# Generated by Django 4.0.6 on 2022-08-19 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournaments', '0006_tournament_created_tournament_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournaments_created', to=settings.AUTH_USER_MODEL),
        ),
    ]
