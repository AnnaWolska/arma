# Generated by Django 3.2.12 on 2023-01-31 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_calculating', '0038_auto_20230131_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='tournament_average',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_disqualifications',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_doubles',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_hands',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_injuries',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_losses',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_opponent_injuries',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_points',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_surrenders',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tournament_wins',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament_calculating.group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='tournament_calculating.participant')),
            ],
        ),
        migrations.AlterField(
            model_name='group',
            name='participants',
            field=models.ManyToManyField(through='tournament_calculating.Participation', to='tournament_calculating.Participant'),
        ),
    ]
