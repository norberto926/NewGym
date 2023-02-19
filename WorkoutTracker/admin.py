from django.contrib import admin

from WorkoutTracker.models import Equipment, Muscle, Exercise

# Register your models here.

admin.site.register(Equipment)
admin.site.register(Muscle)
admin.site.register(Exercise)

