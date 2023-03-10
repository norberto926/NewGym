from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.


# class User(AbstractUser):
#     pass


class Equipment(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Muscle(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    equipment_needed = models.ManyToManyField(Equipment, blank=True)
    main_muscle_group = models.ForeignKey(Muscle, on_delete=models.CASCADE)
    sample = models.BooleanField(default=True)

    class Meta:
        unique_together = ['name', 'owner']

    def __str__(self):
        return self.name


class WorkoutTemplate(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    sample = models.BooleanField(default=False)

    class Meta:
        unique_together = ['owner', 'name']

    def __str__(self):
        return self.name


class Workout(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True)
    template = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE)
    is_template = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)


class WorkoutExercise(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    order = models.IntegerField()


class Set(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    load = models.FloatField(null=True)
    repetitions = models.IntegerField()
    order = models.IntegerField()
    done = models.BooleanField(default=False)





    








