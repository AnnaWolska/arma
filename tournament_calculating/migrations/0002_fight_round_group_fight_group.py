# Generated by Django 4.0.6 on 2022-08-25 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0008_alter_organizer_options'),
        ('tournament_calculating', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rounds', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Walka',
                'verbose_name_plural': 'Walki',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('a', '3'), ('b', '4'), ('c', '5'), ('d', 'remis'), ('e', '0')], max_length=1, null=True)),
                ('fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds_of_fight', to='tournament_calculating.fight')),
            ],
            options={
                'verbose_name': 'Runda',
                'verbose_name_plural': 'Rundy',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('participants', models.ManyToManyField(related_name='groups', to='tournament_calculating.participant')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='tournaments.tournament')),
            ],
            options={
                'verbose_name': 'Grupa',
                'verbose_name_plural': 'Grupy',
            },
        ),
        migrations.AddField(
            model_name='fight',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fights', to='tournament_calculating.group'),
        ),
    ]