import datetime

from django.db import models

# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Muscle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    equipment_needed = models.ManyToManyField(Equipment)
    main_muscle_group = models.ForeignKey(Muscle, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Wset(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    load = models.IntegerField(null=True)
    repetitions = models.IntegerField()
    is_loaded = models.BooleanField(default=True)
    duration = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)


class WorkoutTemplate(models.Model):
    name = models.CharField(max_length=64)
    wsets = models.ManyToManyField(Wset)


class Workout(models.Model):
    date = models.DateField(auto_now_add=True)
    wsets = models.ManyToManyField(Wset)
    start_of_workout = models.TimeField(auto_now_add=True)
    end_of_workout = models.TimeField(null=True)
    comments = models.TextField(null=True)
    workout_template = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE)


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=64)
    workout_templates = models.ManyToManyField(WorkoutTemplate)








