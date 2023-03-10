# Generated by Django 4.1.4 on 2023-03-05 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('WorkoutTracker', '0001_initial'), ('WorkoutTracker', '0002_alter_workoutplan_workout_templates_and_more'), ('WorkoutTracker', '0003_set_created_set_updated_workoutplan_created_and_more'), ('WorkoutTracker', '0004_remove_set_duration_remove_set_is_loaded_and_more'), ('WorkoutTracker', '0005_set_done'), ('WorkoutTracker', '0006_remove_workoutplantemplates_plan_and_more'), ('WorkoutTracker', '0007_alter_exercise_owner_alter_set_owner_and_more'), ('WorkoutTracker', '0008_workouttemplate_finished'), ('WorkoutTracker', '0009_alter_workouttemplate_finished'), ('WorkoutTracker', '0010_remove_workouttemplate_finished_workout_finished'), ('WorkoutTracker', '0011_alter_workout_finished'), ('WorkoutTracker', '0012_alter_exercise_description'), ('WorkoutTracker', '0013_alter_set_load'), ('WorkoutTracker', '0014_alter_exercise_sample_and_more'), ('WorkoutTracker', '0015_alter_workouttemplate_name'), ('WorkoutTracker', '0016_alter_equipment_name_alter_muscle_name_and_more'), ('WorkoutTracker', '0017_alter_exercise_equipment_needed'), ('WorkoutTracker', '0018_remove_set_owner')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('equipment_needed', models.ManyToManyField(to='WorkoutTracker.equipment')),
                ('sample', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Muscle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(null=True)),
                ('is_template', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sample', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='WorkoutExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkoutTracker.exercise')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkoutTracker.workout')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='workout',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkoutTracker.workouttemplate'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='main_muscle_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkoutTracker.muscle'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='workout',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='workout',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='sample',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='exercise',
            unique_together={('name', 'owner')},
        ),
        migrations.AlterField(
            model_name='exercise',
            name='equipment_needed',
            field=models.ManyToManyField(blank=True, to='WorkoutTracker.equipment'),
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('load', models.FloatField(null=True)),
                ('repetitions', models.IntegerField()),
                ('order', models.IntegerField()),
                ('workout_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkoutTracker.workoutexercise')),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('done', models.BooleanField(default=False)),
            ],
        ),
    ]
