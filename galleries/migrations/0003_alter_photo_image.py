# Generated by Django 3.2.12 on 2023-04-06 13:03

from django.db import migrations, models
import galleries.models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0002_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=galleries.models.upload_to),
        ),
    ]
