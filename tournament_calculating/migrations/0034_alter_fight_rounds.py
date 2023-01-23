# Generated by Django 3.2.12 on 2023-01-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_calculating', '0033_alter_group_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fight',
            name='rounds',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0),
        ),
    ]
