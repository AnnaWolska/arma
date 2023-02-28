# Generated by Django 3.2.12 on 2023-02-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_calculating', '0002_auto_20230217_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='color_fighter_one',
            field=models.CharField(choices=[('lemonchiffon', 'żółty'), ('lightgreen', 'zielony'), ('powderblue', 'niebieski'), ('coral', 'czerwony'), ('darkorange', 'pomarańczowy'), ('thistle', 'fioletowy'), ('darkblue', 'granatowy'), ('darkslategray', 'czarny'), ('floralwhite', 'biały'), ('peru', 'brązowy'), ('pink', 'różowy'), ('darkgrey', 'szary')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='color_fighter_two',
            field=models.CharField(choices=[('lemonchiffon', 'żółty'), ('lightgreen', 'zielony'), ('powderblue', 'niebieski'), ('coral', 'czerwony'), ('darkorange', 'pomarańczowy'), ('thistle', 'fioletowy'), ('darkblue', 'granatowy'), ('darkslategray', 'czarny'), ('floralwhite', 'biały'), ('peru', 'brązowy'), ('pink', 'różowy'), ('darkgrey', 'szary')], max_length=30, null=True),
        ),
    ]