# Generated by Django 3.2.12 on 2023-04-06 13:03

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_alter_organizer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='organizers/logos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='tournaments/logos/%Y/%m/%d/'),
        ),
    ]
