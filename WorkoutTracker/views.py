from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from WorkoutTracker.forms import ExerciseForm
from WorkoutTracker.models import Exercise, Equipment, Muscle

# Create your views here.


class AddNewExerciseView(View):
    def get(self, request):
        form = ExerciseForm()
        return render(request, "add_new_exercise.html", {"form": form})

    def post(self, request):
        form = ExerciseForm(request.POST)
        if form.is_valid():
            new_exercise = form.save()
            return HttpResponse('Exercise saved')



