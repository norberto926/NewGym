# Generated by Django 4.1.4 on 2023-02-16 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutTracker', '0004_remove_set_duration_remove_set_is_loaded_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
