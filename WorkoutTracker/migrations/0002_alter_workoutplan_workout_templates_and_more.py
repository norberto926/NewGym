# Generated by Django 4.1.4 on 2023-01-18 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutTracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutplan',
            name='workout_templates',
            field=models.ManyToManyField(through='WorkoutTracker.WorkoutPlanTemplates', to='WorkoutTracker.workouttemplate'),
        ),
        migrations.AlterField(
            model_name='workoutplantemplates',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkoutTracker.workouttemplate'),
        ),
    ]
