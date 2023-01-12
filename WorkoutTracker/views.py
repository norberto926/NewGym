from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from WorkoutTracker.filters import ExerciseFilter
from WorkoutTracker.forms import ExerciseForm, WorkoutTemplateForm, SetFormWorkoutTemplate, WorkoutPlanForm
from WorkoutTracker.models import Exercise, Equipment, Muscle, Workout, WorkoutPlan, WorkoutTemplate, \
    WorkoutPlanTemplates, Set

# Create your views here.


def display_workout(workout):
    sets = Set.objects.filter(workout=workout)
    workout_dict = {}
    for set in sets:
        if set.exercise in workout_dict.keys():
            workout_dict[set.exercise].append(set)
        else:
            workout_dict[set.exercise] = [set]
    for element in workout_dict.items():
        element[1].sort(key=lambda x: x.created)
    return workout_dict


class CreateExercise(View):
    def get(self, request):
        form = ExerciseForm()
        return render(request, "create_exercise.html", {"form": form})

    def post(self, request):
        exercise_form = ExerciseForm(request.POST)
        if exercise_form.is_valid():
            exercise_form.save()
            return HttpResponse('Exercise saved')


class CreateWorkoutTemplate(View):

    def get(self, request):
        workout_template_form = WorkoutTemplateForm()
        return render(request, 'new_workout_template.html', {'workout_template_form': workout_template_form})

    def post(self, request):
        workout_template_form = WorkoutTemplateForm(request.POST)
        if workout_template_form.is_valid():
            new_workout_template = workout_template_form.save()
            new_workout = Workout.objects.create(is_template=True, template=new_workout_template)
            return HttpResponse('Workout template created')


class EditWorkoutTemplate(View):

    def get(self, request, workout_template_id):
        request.session['workout_template_id'] = workout_template_id
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        workout = Workout.objects.get(template=workout_template, is_template=True)
        workout_dict = display_workout(workout)
        ctx = {'workout_template': workout_template,
               'workout_dict': workout_dict}
        return render(request, 'edit_workout_template.html', ctx)

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

        exercise_id = int(request.POST.get("exercise_id"))
        request.session['exercise_id'] = exercise_id
        return redirect('create_set')


class CreateSetForWorkoutTemplate(View):

    def get(self, request):
        set_form_workout_template = SetFormWorkoutTemplate()
        if request.session.get('last_set_repetition_number'):
            last_set_repetition_number = int(request.session.get('last_set_repetition_number'))
            set_form_workout_template = SetForm(initial={'repetitions': last_set_repetition_number})
        exercise_id = int(request.session.get('exercise_id'))
        exercise = Exercise.objects.get(id=exercise_id)
        return render(request, 'create_set.html', {'set_form_workout_template': set_form_workout_template, 'exercise': exercise})

    def post(self, request):
        set_form = SetFormWorkoutTemplate(request.POST)
        workout_template_id = int(request.session.get("workout_template_id"))
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        if set_form.is_valid():
            new_set = set_form.save(commit=False)
            exercise_id = int(request.session.get('exercise_id'))
            exercise = Exercise.objects.get(id=exercise_id)
            new_set.exercise = exercise
            workout = Workout.objects.get(template=workout_template, is_template=True)
            new_set.workout = workout
            new_set.save()
            request.session["last_set_repetition_number"] = new_set.repetitions
        return redirect('edit_workout_template', workout_template_id=workout_template_id)


class CreateWorkoutPlan(View):

    def get(self, request):
        workout_plan_form = WorkoutPlanForm()
        ctx = {
            'workout_plan_form': workout_plan_form
        }
        return render(request, 'create_workout_plan.html', {'ctx': ctx})

    def post(self, request):
        workout_plan_form = WorkoutPlanForm(request.POST)
        if workout_plan_form.is_valid():
            workout_plan_form.save()
        return HttpResponse("Workout plan created")


class MainPageView(View):
    def get(self, request):
        last_workout = Workout.objects.order_by('-date')[0]
        active_plan = WorkoutPlan.objects.get(is_active=True)
        order_in_plan_of_last_workout = WorkoutPlanTemplates.objects.get(template=last_workout.template, plan=active_plan).order
        # need to add back to first template condition
        next_workout_template = WorkoutPlanTemplates.objects.get(order=order_in_plan_of_last_workout + 1).template
        last_workout_with_next_workout_template = Workout.objects.filter(template=next_workout_template).order_by('-created')[0]
        request.session['last_workout_with_next_workout_template'] = last_workout_with_next_workout_template


class WorkoutPlanList(View):
    def get(self, request):
        workout_plan_list = WorkoutPlan.objects.all()
        ctx = {
            'workout_plan_list': workout_plan_list
        }
        return render(request, "workout_plan_list.html", ctx )

    def post(self, request):
        all_workout_plans = WorkoutPlan.objects.all()
        for plan in all_workout_plans:
            plan.is_active = False
        workout_plan_id = request.POST.get('workout_plan_id')
        workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
        workout_plan.is_active = True
        return redirect('workout_plan_list')





















