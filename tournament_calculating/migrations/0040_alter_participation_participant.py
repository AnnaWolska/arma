# Generated by Django 3.2.12 on 2023-01-31 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_calculating', '0039_auto_20230131_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament_calculating.participant'),
        ),
    ]
