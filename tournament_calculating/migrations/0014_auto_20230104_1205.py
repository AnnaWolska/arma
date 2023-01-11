# Generated by Django 3.2.12 on 2023-01-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_calculating', '0013_auto_20230104_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='color_fighter_one',
            field=models.CharField(choices=[('żółty', 'lemonchiffon'), ('zielony', 'lightgreen'), ('niebieski', 'powderblue'), ('czerwony', 'coral'), ('pomarańczowy', 'darkorange'), ('fioletowy', 'thistle'), ('granatowy', 'darkblue'), ('czarny', 'darkslategray'), ('biały', 'floralwhite'), ('brązowy', 'peru'), ('różowy', 'pink'), ('szary', 'darkgrey')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='color_fighter_two',
            field=models.CharField(choices=[('żółty', 'lemonchiffon'), ('zielony', 'lightgreen'), ('niebieski', 'powderblue'), ('czerwony', 'coral'), ('pomarańczowy', 'darkorange'), ('fioletowy', 'thistle'), ('granatowy', 'darkblue'), ('czarny', 'darkslategray'), ('biały', 'floralwhite'), ('brązowy', 'peru'), ('różowy', 'pink'), ('szary', 'darkgrey')], max_length=30, null=True),
        ),
    ]