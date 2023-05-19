# Generated by Django 3.2.12 on 2023-04-06 13:03

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_calculating', '0013_alter_participant_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='tournament_calculating/images/%Y/%m/%d/'),
        ),
    ]
