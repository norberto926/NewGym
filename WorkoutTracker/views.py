from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from WorkoutTracker.forms import ExerciseForm, WorkoutTemplateForm, WorkoutForTemplateForm
from WorkoutTracker.models import Exercise, Equipment, Muscle, Workout, WorkoutTemplate

# Create your views here.


class AddNewExerciseView(View):
    def get(self, request):
        form = ExerciseForm()
        return render(request, "add_new_exercise.html", {"form": form})

    def post(self, request):
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Exercise saved')


class AddNewWorkoutTemplateView(View):

    def get(self, request):
        workout_form = WorkoutForTemplateForm()
        workout_template_form = WorkoutTemplateForm()
        return render(request, 'new_workout_template.html', {'workout_form': workout_form, 'workout_template_form': workout_template_form})

    def post(self, request):
        workout_form = WorkoutForTemplateForm(request.POST)
        workout_template_form = WorkoutTemplateForm(request.POST)
        if workout_form.is_valid() and workout_template_form.is_valid():
            workout = workout_form.save(commit=False)
            workout.is_template = True
            workout.save()
            workout_template = workout_template_form.save(commit=False)
            workout_template.workout = workout
            workout_template.save()
            return HttpResponse('Workout template created')


class EditWorkoutTemplateView(View):

    def get(self, request, workout_template_id):
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        workout = workout_template.workout
        set_dict = {}
        for set in workout.sets:
            if set.exercise in set_dict.keys():
                set_dict[set.exercise].append(set)
            else:
                set_dict[set.exercise] = [set]
        return render(request, 'edit_workout_template.html', {'workout_template': workout_template, 'set_dict': set_dict})







