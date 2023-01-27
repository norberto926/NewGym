from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from WorkoutTracker.filters import ExerciseFilter
from WorkoutTracker.forms import ExerciseForm, WorkoutTemplateForm, SetFormWorkoutTemplate, WorkoutPlanForm, \
    CreateSetForWorkoutExerciseForWorkoutForm
from WorkoutTracker.models import Exercise, Equipment, Muscle, Workout, WorkoutPlan, WorkoutTemplate, \
    WorkoutPlanTemplates, Set, WorkoutExercise



# Create your views here.


def progression_calc(workout_base_set, workout_exercise, set_order):
    workout_template = workout_base_set.workout_exercise.workout.template  # do this or pass a parameter
    workout_for_workout_template = Workout.objects.get(template=workout_template, is_template=True)
    workout_exercise_for_workout = WorkoutExercise.objects.get(workout=workout_for_workout_template,
                                                               order=workout_base_set.workout_exercise.order)
    if int(set_order) == 1:
        template_set = Set.objects.get(workout_exercise=workout_exercise_for_workout, order=1)
        if workout_base_set.repetitions == template_set.repetitions:
            return workout_base_set.load + 5, workout_base_set.repetitions
        else:
            return workout_base_set.load, template_set.repetitions
    else:
        previous_set_order = int(set_order) - 1
        previous_set = Set.objects.get(workout_exercise=workout_exercise, order=int(set_order) - 1)






def create_workout_display(workout):
    workout_exercises = WorkoutExercise.objects.filter(workout=workout).order_by('order')
    set_dict = {}
    for workout_exercise in workout_exercises:
        set_dict[workout_exercise] = Set.objects.filter(workout_exercise=workout_exercise).order_by('order')
    return set_dict

def calculate_totals_for_workout(workout):
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)
    total_sets = 0
    total_load = 0
    total_repetitions = 0
    for workout_exercise in workout_exercises:
        workout_exercise_sets = Set.objects.filter(workout_exercise=workout_exercise)
        for set in workout_exercise_sets:
            total_sets += 1
            total_repetitions += set.repetitions
            total_load += set.load
    return total_sets, total_repetitions, total_load




class CreateExercise(View):
    def get(self, request, *args, **kwargs):
        form = ExerciseForm()
        return render(request, "create_exercise.html", {"form": form})

    def post(self, request, *args, **kwargs):
        exercise_form = ExerciseForm(request.POST)
        if exercise_form.is_valid():
            exercise_form.save()
            return redirect('add_exercise_to_workout_template')


class CreateWorkoutTemplate(View):

    def get(self, request):
        workout_template_form = WorkoutTemplateForm()
        return render(request, 'create_workout_template.html', {'workout_template_form': workout_template_form})

    def post(self, request):
        workout_template_form = WorkoutTemplateForm(request.POST)
        if workout_template_form.is_valid():
            new_workout_template = workout_template_form.save()
            new_workout = Workout.objects.create(is_template=True, template=new_workout_template)
            return redirect('edit_workout_template', workout_template_id=new_workout_template.id)


class EditWorkoutTemplate(View):

    def get(self, request, workout_template_id):
        request.session['workout_template_id'] = workout_template_id
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        workout = Workout.objects.get(template=workout_template, is_template=True)
        workout_exercises = WorkoutExercise.objects.filter(workout=workout).order_by('order')
        set_dict = {}
        for workout_exercise in workout_exercises:
            set_dict[workout_exercise] = Set.objects.filter(workout_exercise=workout_exercise).order_by('order')

        ctx = {'workout_template': workout_template,
               'set_dict': set_dict
               }
        return render(request, 'edit_workout_template.html', ctx)

    def post(self, request, workout_template_id):
        workout_exercise_id = int(request.POST.get("workout_exercise_id"))
        request.session['exercise_id'] = workout_exercise_id
        return redirect('create_set', workout_exercise_id=workout_exercise_id)


class AddExerciseToWorkoutTemplate(View):

    def get(self, request):

        exercise_list = Exercise.objects.all()
        exercise_filter = ExerciseFilter(request.GET, queryset=exercise_list)

        return render(request, "add_exercise_to_workout_template.html", {"exercise_filter": exercise_filter})

    def post(self, request):

        workout_template_id = request.session.get('workout_template_id')
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        workout = Workout.objects.get(template=workout_template, is_template=True)
        exercise_id = int(request.POST.get("exercise_id"))
        exercise = Exercise.objects.get(id=exercise_id)
        exercises_in_workout = WorkoutExercise.objects.filter(workout=workout)
        if not exercises_in_workout:
            new_workout_exercise = WorkoutExercise.objects.create(exercise=exercise, workout=workout, order=1)
        else:
            new_workout_exercise = WorkoutExercise.objects.create(exercise=exercise, workout=workout, order=len(exercises_in_workout) + 1)
        request.session['workout_exercise_id'] = new_workout_exercise.id
        return redirect('create_set', workout_exercise_id=new_workout_exercise.id)


class CreateSetForWorkoutExercise(View):

    def get(self, request, workout_exercise_id):
        set_form_workout_template = SetFormWorkoutTemplate()
        if request.session.get('last_set_repetition_number'):
            last_set_repetition_number = int(request.session.get('last_set_repetition_number'))
            set_form_workout_template = SetFormWorkoutTemplate(initial={'repetitions': last_set_repetition_number})
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        return render(request, 'create_set.html', {'set_form_workout_template': set_form_workout_template, 'workout_exercise': workout_exercise})

    def post(self, request, workout_exercise_id):
        set_form = SetFormWorkoutTemplate(request.POST)
        workout_template_id = int(request.session.get("workout_template_id"))
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        if set_form.is_valid():
            new_set = set_form.save(commit=False)
            workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
            new_set.workout_exercise = workout_exercise
            exercise_sets = Set.objects.filter(workout_exercise=workout_exercise)
            if exercise_sets:
                new_set.order = len(exercise_sets) + 1
            else:
                new_set.order = 1
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
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_workout_plan = WorkoutPlan.objects.create(name=name)

            return redirect('edit_workout_plan', workout_plan_id=new_workout_plan.id)


class EditWorkoutPlan(View):
    def get(self, request, workout_plan_id):
        workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
        request.session['workout_plan_id'] = workout_plan_id
        return render(request, 'edit_workout_plan.html', {'workout_plan': workout_plan})

    def post(self, request, workout_plan_id):
        workout_plan = WorkoutPlan.objects.get(workout_plan_id)
        return redirect('add_workout_template_to_workout_plan')


class AddWorkoutTemplateToWorkoutPlan(View):
    def get(self, request):
        all_templates = WorkoutTemplate.objects.all()
        return render(request, 'add_workout_template_to_workout_plan.html', {'all_templates': all_templates})

    def post(self, request):
        workout_plan_id = request.session.get('workout_plan_id')
        workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
        workout_template_id = request.POST.get('workout_template_id')
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        templates_in_plan = WorkoutPlanTemplates.objects.filter(plan=workout_plan)
        if templates_in_plan:
            new_workout_plan_template = WorkoutPlanTemplates.objects.create(plan=workout_plan, template=workout_template,
                                                                            order=len(templates_in_plan) + 1)
        else:
            new_workout_plan_template = WorkoutPlanTemplates.objects.create(plan=workout_plan, template=workout_template,
                                                                            order=1)

        return redirect('edit_workout_plan', workout_plan_id=workout_plan_id)


class MainPageView(View):
    def get(self, request):
        last_workout = Workout.objects.order_by('-created')[0]
        active_plan = WorkoutPlan.objects.get(is_active=True)
        order_in_plan_of_last_workout = WorkoutPlanTemplates.objects.get(template=last_workout.template, plan=active_plan).order
        all_templates_in_plan = WorkoutPlanTemplates.objects.filter(plan=active_plan).order_by('order')
        if order_in_plan_of_last_workout == all_templates_in_plan.last().order:
            next_workout_template = WorkoutPlanTemplates.objects.get(order=1, plan=active_plan).template
        else:
            next_workout_template = WorkoutPlanTemplates.objects.get(order=order_in_plan_of_last_workout + 1, plan=active_plan).template
        next_workout = Workout.objects.get(template=next_workout_template, is_template=True)
        request.session['workout_base_template_id'] = next_workout_template.id
        ctx = {
            'last_workout_dict': create_workout_display(last_workout),
            'last_workout': last_workout,
            'last_workout_totals': calculate_totals_for_workout(last_workout),
            'next_workout_dict': create_workout_display(next_workout),
            'next_workout': next_workout,
            'active_plan': active_plan

        }
        return render(request, 'main.html', ctx)


class WorkoutPlanList(View):

    def get(self, request):
        workout_plan_list = WorkoutPlan.objects.all().order_by('-created')
        ctx = {
            'workout_plan_list': workout_plan_list
        }
        return render(request, "workout_plan_list.html", ctx)

    def post(self, request):
        all_workout_plans = WorkoutPlan.objects.all().order_by('-created')
        for workout_plan in all_workout_plans:
            workout_plan.is_active = False
            workout_plan.save()
        workout_plan_id = int(request.POST.get('workout_plan_id'))
        workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
        workout_plan.is_active = True
        workout_plan.save()
        return redirect('workout_plan_list')


class CreateNewWorkout(View):

    def get(self, request):
        workout_template_id = int(request.session.get('workout_base_template_id'))
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id)
        workout_base = Workout.objects.filter(template=workout_template).order_by('-created')[0]
        workout_base_exercises = WorkoutExercise.objects.filter(workout=workout_base)
        new_workout = Workout.objects.create(template=workout_template)
        exercise_order = 1
        return redirect('create_workout_exercise_for_workout', new_workout_id=new_workout.id, workout_base_id=workout_base.id, exercise_order=1)


class CreateWorkoutExerciseForWorkout(View):

    def get(self, request, new_workout_id, workout_base_id, exercise_order):
        workout_base = Workout.objects.get(id=workout_base_id)
        workout_base_exercise = WorkoutExercise.objects.get(workout=workout_base, order=exercise_order)
        new_workout = Workout.objects.get(id=new_workout_id)
        new_workout_exercise = WorkoutExercise.objects.create(workout=new_workout, exercise=workout_base_exercise.exercise, order=exercise_order)
        set_order = 1
        return redirect('create_set_for_workout_exercise_for_workout', workout_base_exercise_id=workout_base_exercise.id, workout_exercise_id=new_workout_exercise.id, set_order=set_order)


class CreateSetForWorkoutExerciseForWorkout(View):
    def get(self, request, workout_base_exercise_id, workout_exercise_id, set_order):
        workout_base_exercise = WorkoutExercise.objects.get(id=workout_base_exercise_id)
        workout_base_set = Set.objects.get(workout_exercise=workout_base_exercise, order=set_order)
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
        form = CreateSetForWorkoutExerciseForWorkoutForm(initial={'load': workout_base_set.load,
                                                                  'repetitions': workout_base_set.repetitions})

        return render(request, 'create_set_for_workout_exercise_for_workout.html', {'form': form, 'workout_exercise': workout_exercise})

    def post(self, request, workout_base_exercise_id, workout_exercise_id, set_order):
        form = CreateSetForWorkoutExerciseForWorkoutForm(request.POST)
        if form.is_valid():
            load = form.cleaned_data['load']
            repetitions = form.cleaned_data['repetitions']
            workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_id)
            new_set = Set.objects.create(workout_exercise=workout_exercise, load=load, repetitions=repetitions, order=set_order)
            workout_base_exercise = WorkoutExercise.objects.get(id=workout_base_exercise_id)
            workout_base_exercise_sets = Set.objects.filter(workout_exercise=workout_base_exercise).order_by('order')
            if workout_base_exercise_sets.last().order == int(set_order):
                workout_base_exercises = WorkoutExercise.objects.filter(workout=workout_base_exercise.workout).order_by('order')
                if workout_base_exercises.last().order == workout_base_exercise.order:
                    return redirect('edit_workout', workout_id=workout_exercise.workout.id)
                else:
                    return redirect('create_workout_exercise_for_workout', workout_base_id=workout_base_exercise.workout.id,
                                    new_workout_id=workout_exercise.workout.id, exercise_order=workout_exercise.order + 1)
            else:
                return redirect('create_set_for_workout_exercise_for_workout', workout_base_exercise_id=workout_base_exercise_id,
                         workout_exercise_id=workout_exercise_id, set_order=int(set_order) + 1)


class EditWorkout(View):

    def get(self, request, workout_id):
        workout = Workout.objects.get(id=workout_id)
        workout_exercises = WorkoutExercise.objects.filter(workout=workout).order_by('order')
        set_dict = {}
        for workout_exercise in workout_exercises:
            set_dict[workout_exercise] = Set.objects.filter(workout_exercise=workout_exercise).order_by('order')

        ctx = {'workout': workout,
               'set_dict': set_dict
               }
        return render(request, 'edit_workout.html', ctx)



                    

































