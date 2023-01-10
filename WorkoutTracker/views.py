from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_filters.views import FilterView

from WorkoutTracker.filters import ExerciseFilter
from WorkoutTracker.forms import ExerciseForm, WorkoutTemplateForm, WsetForm
from WorkoutTracker.models import Exercise, Equipment, Muscle, Workout, WorkoutTemplate
from WorkoutTracker.models import Wset
from django.views.generic.list import ListView

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
        workout_template_form = WorkoutTemplateForm()
        return render(request, 'new_workout_template.html', {'workout_template_form': workout_template_form})

    def post(self, request):
        workout_template_form = WorkoutTemplateForm(request.POST)
        if workout_template_form.is_valid():
            workout_template = workout_template_form.save(commit=False)
            workout_template.save()
            return HttpResponse('Workout template created')


class EditWorkoutTemplateView(View):

    def get(self, request, workout_template_id):
        request.session['workout_template_id'] = workout_template_id
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        wset_dict = {}
        for wset in workout_template.wsets.all():
            if wset.exercise in wset_dict.keys():
                wset_dict[wset.exercise].append(wset)
            else:
                wset_dict[wset.exercise] = [wset]
        return render(request, 'edit_workout_template.html', {'workout_template': workout_template, 'wset_dict': wset_dict})

    def post(self, request, workout_template_id):
        exercise_id = int(request.POST.get("exercise_id"))
        exercise = Exercise.objects.get(id=exercise_id)
        return redirect('create_set', exercise_id=exercise_id)



class AddExerciseToWorkoutTemplate(View):

    def get(self, request):

        exercise_list = Exercise.objects.all()
        exercise_filter = ExerciseFilter(request.GET, queryset=exercise_list)

        return render(request, "add_exercise_to_workout_template.html", {"exercise_filter": exercise_filter})

    def post(self, request):

        workout_template_id = int(request.session.get("workout_template_id"))
        exercise_id = int(request.POST.get("exercise_id"))
        # return redirect("edit_workout_template_id", workout_template_id=workout_template_id)
        return redirect('create_set', exercise_id=exercise_id)


class CreateWset(View):

    def get(self, request, exercise_id):
        wset_form = WsetForm()
        if request.session.get('last_wset_repetition_number'):
            last_wset_repetition_number = int(request.session.get('last_wset_repetition_number'))
            wset_form = WsetForm(initial={'repetitions': last_wset_repetition_number})
        exercise = Exercise.objects.get(id=exercise_id)
        return render(request, 'create_set.html', {'wset_form': wset_form, 'exercise': exercise})

    def post(self, request, exercise_id):
        wset_form = WsetForm(request.POST)
        exercise_id = int(request.POST.get("exercise_id"))
        exercise = Exercise.objects.get(id=exercise_id)
        workout_template_id = int(request.session.get("workout_template_id"))
        if wset_form.is_valid():
            new_wset = wset_form.save(commit=False)
            new_wset.exercise = Exercise.objects.get(id=exercise_id)
            new_wset.save()
            workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
            workout = workout_template.workout
            workout.wsets.add(new_wset)
            request.session["last_wset_repetition_number"] = new_wset.repetitions
        return redirect('edit_workout_template', workout_template_id=workout_template_id)




















