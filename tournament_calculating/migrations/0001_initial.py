# Generated by Django 3.2.12 on 2022-12-02 13:12

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tournaments', '0001_initial'),
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
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=500)),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='tournament_calculating/images/%Y/%m/%d/')),
                ('tournaments', models.ManyToManyField(related_name='participants', to='tournaments.Tournament')),
            ],
            options={
                'verbose_name': 'Zawodnik',
                'verbose_name_plural': 'Zawodnicy',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('0', 'win'), ('1', 'lose'), ('2', 'remis'), ('3', 'no result'), ('4', 'no fight')], max_length=1, null=True)),
                ('points', models.PositiveSmallIntegerField(null=True)),
                ('fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds_of_fight', to='tournament_calculating.fight')),
                ('fighter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fighter', to='tournament_calculating.participant')),
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
                ('participants', models.ManyToManyField(related_name='groups', to='tournament_calculating.Participant')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='tournaments.tournament')),
            ],
            options={
                'verbose_name': 'Grupa',
                'verbose_name_plural': 'Grupy',
            },
        ),
        migrations.AddField(
            model_name='fight',
            name='fighter_one',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fighters_one', to='tournament_calculating.participant'),
        ),
        migrations.AddField(
            model_name='fight',
            name='fighter_two',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fighters_two', to='tournament_calculating.participant'),
        ),
        migrations.AddField(
            model_name='fight',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fights', to='tournament_calculating.group'),
        ),
        migrations.AddField(
            model_name='fight',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fights', to='tournaments.tournament'),
        ),
    ]
