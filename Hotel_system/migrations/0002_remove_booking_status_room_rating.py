# Generated by Django 5.1 on 2024-08-16 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='status',
        ),
        migrations.AddField(
            model_name='room',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
    ]
