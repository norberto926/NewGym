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
    template = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE)
    is_template = models.BooleanField(default=False)


class WorkoutExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    order = models.IntegerField()


class Set(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    load = models.IntegerField(null=True)
    repetitions = models.IntegerField()
    order = models.IntegerField()
    duration = models.IntegerField(null=True, blank=True)
    is_loaded = models.BooleanField(default=True)


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=64)
    workout_templates = models.ManyToManyField(Workout, through='WorkoutPlanTemplates')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WorkoutPlanTemplates(models.Model):
    template = models.ForeignKey(Workout, on_delete=models.CASCADE)
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    order = models.IntegerField()
    








