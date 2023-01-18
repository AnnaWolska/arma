# Generated by Django 3.2.12 on 2023-01-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_calculating', '0031_auto_20230118_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='points_fighter_one',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('0 dubl', '0 dubl'), ('kontuzja', 'kontuzja'), ('dyskwalifikacja', 'dyskwalifikacja'), ('poddanie', 'poddanie'), ('wycofanie', 'wycofanie'), ('średnia', 'średnia')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='points_fighter_two',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('0 dubl', '0 dubl'), ('kontuzja', 'kontuzja'), ('dyskwalifikacja', 'dyskwalifikacja'), ('poddanie', 'poddanie'), ('wycofanie', 'wycofanie'), ('średnia', 'średnia')], max_length=20, null=True),
        ),
    ]
