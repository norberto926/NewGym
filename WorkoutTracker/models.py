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


class WorkoutTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True)
    template = models.ForeignKey(WorkoutTemplate)
    is_template = models.BooleanField(default=False)


class Set(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    load = models.IntegerField(null=True)
    repetitions = models.IntegerField()
    is_loaded = models.BooleanField(default=True)
    duration = models.IntegerField(null=True)


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=64)
    workout_templates = models.ManyToManyField(Workout, through='WorkoutPlanTemplates')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WorkoutPlanTemplates(models.Model):
    template = models.ForeignKey(Workout)
    plan = models.ForeignKey(WorkoutPlan)
    order = models.IntegerField()
    








