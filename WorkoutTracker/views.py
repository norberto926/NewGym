import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.views import View
from django.db import IntegrityError
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from WorkoutTracker.database_population import populate_exercises_on_registration, populate_templates_on_registration
from WorkoutTracker.filters import ExerciseFilter
from WorkoutTracker.forms import ExerciseForm, WorkoutTemplateForm, SetFormWorkoutTemplate, SetFormWorkout, RegisterForm
from WorkoutTracker.models import Exercise, Workout, WorkoutTemplate, Set, WorkoutExercise


# Create your views here.


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
            if set.load:
                total_load += set.load
    return total_sets, total_repetitions, total_load


class CreateExercise(View):
    def get(self, request):
        form = ExerciseForm()
        return render(request, "create_exercise.html", {"form": form})

    def post(self, request):
        form = ExerciseForm(request.POST)
        form.instance.owner = request.user
        form.instance.sample = False
        if form.is_valid():
            try:
                new_exercise = form.save()
            except IntegrityError:
                return render(request, 'create_exercise.html', {'form': form, 'error_message': 'Exercise with this name already exists'})
            if form.cleaned_data.get('equipment_needed'):
                for el in form.cleaned_data['equipment_needed']:
                    new_exercise.equipment_needed.add(el)
            return redirect('exercise_list')
        return render(request, 'create_exercise.html', {'form': form})


class DeleteExercise(View):
    def get(self, request, exercise_pk):
        exercise = Exercise.objects.get(id=exercise_pk)
        if exercise:
            exercise.delete()
            return redirect('exercise_list')


class MainPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            ctx = {}
            unfinished_workouts_with_archived = Workout.objects.filter(finished=False, owner=request.user)
            unfinished_workouts = []
            for workout in unfinished_workouts_with_archived:
                if not workout.template.is_archived:
                    unfinished_workouts.append(workout)
            if unfinished_workouts:
                ctx['unfinished_workouts'] = unfinished_workouts
            if Workout.objects.filter(owner=request.user, is_template=False):
                last_workout = Workout.objects.filter(is_template=False, owner=request.user).order_by('-created')[0]
                ctx['last_workout_dict'] = create_workout_display(last_workout)
                ctx['last_workout'] = last_workout
                ctx['last_workout_totals'] = calculate_totals_for_workout(last_workout)
                return render(request, 'main.html', ctx)
        return render(request, 'main.html')


class CreateUser(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/sign_up.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            populate_exercises_on_registration(request)
            populate_templates_on_registration(request)
            return redirect('/main')
        return render(request, 'registration/sign_up.html', {'form': form})


class CreateWorkoutTemplate(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        workout_template_form = WorkoutTemplateForm()
        return render(request, 'create_workout_template.html', {'workout_template_form': workout_template_form})

    def post(self, request):
        workout_template_form = WorkoutTemplateForm(request.POST)
        if workout_template_form.is_valid():
            new_workout_template = workout_template_form.save(commit=False)
            new_workout_template.owner = request.user
            try:
                new_workout_template.save()
            except IntegrityError:
                return render(request, 'create_workout_template.html', {'workout_template_form': workout_template_form, 'error_message': 'Template with this name already exists'})
            new_workout = Workout.objects.create(is_template=True, template=new_workout_template, owner=request.user)
            return redirect('edit_workout_template', workout_template_pk=new_workout_template.pk)
        return render(request, 'create_workout_template.html', {'workout_template_form': workout_template_form})


@login_required
def edit_workout_template(request, workout_template_pk):
    workout_template = WorkoutTemplate.objects.get(pk=workout_template_pk, owner=request.user)
    template_form = WorkoutTemplateForm(instance=workout_template)
    workout = Workout.objects.get(template=workout_template, is_template=True, owner=request.user)
    workout_exercises = WorkoutExercise.objects.filter(workout=workout, owner=request.user)
    SetFormset = inlineformset_factory(WorkoutExercise, Set, form=SetFormWorkoutTemplate, can_delete=True, extra=0)
    workout_dict = {}
    if request.method == 'GET':
        for exercise in workout_exercises:
            formset = SetFormset(instance=exercise, prefix=exercise.exercise)
            workout_dict[exercise] = formset
        ctx = {'template_form': template_form,
                   'workout_dict': workout_dict
                }
        return render(request, 'edit_workout_template.html', ctx)

    if request.method == 'POST':
        template_form = WorkoutTemplateForm(request.POST, instance=workout_template)
        if template_form.is_valid():
            template_form.save()
        for exercise in workout_exercises:
            formset = SetFormset(request.POST, instance=exercise, prefix=exercise.exercise)
            for index, form in enumerate(formset):
                if form.is_valid():
                    new_set = form.save(commit=False)
                    new_set.owner = request.user
                    if not new_set.order:
                        new_set.order = index + 1
                    if new_set.repetitions:
                        form.save()
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            sets = Set.objects.filter(workout_exercise=exercise, owner=request.user)
            if not sets:
                exercise.delete()
            workout_exercises = WorkoutExercise.objects.filter(workout=workout, owner=request.user)
            if workout_exercises:
                workout.finished = True
                workout.save()
            return redirect('/main')
        return redirect('workout_template_list')


class WorkoutTemplateList(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        workout_template_list = WorkoutTemplate.objects.filter(is_archived=False, owner=request.user).order_by('-created')
        workout_template_dict = {}
        for workout_template in workout_template_list:
            workout = Workout.objects.get(template=workout_template, is_template=True)
            all_exercises = WorkoutExercise.objects.filter(workout=workout, owner=request.user)
            all_sets_count = 0
            for workout_exercise in all_exercises:
                set_count = Set.objects.filter(workout_exercise=workout_exercise, owner=request.user).count()
                all_sets_count += set_count
            workouts_done_with_template = Workout.objects.filter(template=workout_template, is_template=False, owner=request.user).order_by('-created')
            if len(workouts_done_with_template) == 0:
                last_workout_with_template = ""
                total_workouts_done_with_template = 0
            else:
                last_workout_with_template = workouts_done_with_template.first().created
                total_workouts_done_with_template = workouts_done_with_template.count()
            workout_template_dict[workout_template] = {'all_exercises': all_exercises, 'all_sets_count': all_sets_count,
                                                        'last_workout_with_template': last_workout_with_template,
                                                        'total_workouts_done_with_template': total_workouts_done_with_template}
        ctx = {
            'workout_template_dict': workout_template_dict,
        }
        return render(request, "workout_template_list.html", ctx)


class ExerciseList(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):

        exercise_list = Exercise.objects.filter(owner=request.user).order_by('name')
        exercise_filter = ExerciseFilter(request.GET, queryset=exercise_list)
        ctx = {
            "exercise_filter": exercise_filter
        }

        return render(request, "exercise_list.html", ctx)


class AddExercise(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, workout_template_pk):
        exercise_list = Exercise.objects.filter(owner=request.user).order_by('name')
        exercise_filter = ExerciseFilter(request.GET, queryset=exercise_list)
        workout_template_pk = request.GET.get('workout_template_id')
        ctx = {
            "exercise_filter": exercise_filter,
            "workout_template_pk": workout_template_pk
        }

        return render(request, "add_exercise.html", ctx)
    def post(self, request, workout_template_pk):
        workout_template = WorkoutTemplate.objects.get(id=workout_template_pk)
        workout = Workout.objects.get(template=workout_template, is_template=True, owner=request.user)
        exercise_id = int(request.POST.get("exercise_pk"))
        exercise = Exercise.objects.get(id=exercise_id, owner=request.user)
        exercises_in_workout = WorkoutExercise.objects.filter(workout=workout, owner=request.user)
        for workout_exercise in exercises_in_workout:
            if workout_exercise.exercise == exercise:
                return redirect('edit_workout_template', workout_template_pk=workout_template_pk) # jak zrobić to przekierowanie z komunikatem
        new_workout_exercise = WorkoutExercise.objects.create(exercise=exercise, workout=workout, order=len(exercises_in_workout) + 1, owner=request.user)
        return redirect('edit_workout_template', workout_template_pk=workout_template_pk)


class DeleteWorkoutExercise(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, workout_template_pk, workout_exercise_pk):
        workout_exercise = WorkoutExercise.objects.get(id=workout_exercise_pk, owner=request.user)
        workout_exercise.delete()
        return redirect('edit_workout_template', workout_template_pk=workout_template_pk)


class ArchiveTemplate(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, workout_template_pk):
        workout_template = WorkoutTemplate.objects.get(id=workout_template_pk, owner=request.user)
        workout_template.is_archived = True
        workout_template.save()
        return redirect('workout_template_list')


class CreateWorkout(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        workout_template_list = WorkoutTemplate.objects.filter(is_archived=False, owner=request.user).order_by('-created')
        workout_template_dict = {}
        for workout_template in workout_template_list:
            workout = Workout.objects.get(template=workout_template, is_template=True)
            all_exercises = WorkoutExercise.objects.filter(workout=workout)
            all_sets_count = 0
            for workout_exercise in all_exercises:
                set_count = Set.objects.filter(workout_exercise=workout_exercise, owner=request.user).count()
                all_sets_count += set_count
            workouts_done_with_template = Workout.objects.filter(template=workout_template, is_template=False, owner=request.user).order_by('-created')
            if len(workouts_done_with_template) == 0:
                last_workout_with_template = ""
                total_workouts_done_with_template = 0
            else:
                last_workout_with_template = workouts_done_with_template.first().created
                total_workouts_done_with_template = workouts_done_with_template.count()
            workout_template_dict[workout_template] = {'all_exercises': all_exercises, 'all_sets_count': all_sets_count,
                                                        'last_workout_with_template': last_workout_with_template,
                                                        'total_workouts_done_with_template': total_workouts_done_with_template}
        ctx = {
            'workout_template_dict': workout_template_dict,
        }
        return render(request, "create_workout.html", ctx)

    def post(self, request):
        workout_template_id = int(request.POST.get('workout_template_pk'))
        workout_template = WorkoutTemplate.objects.get(id=workout_template_id, owner=request.user)
        new_workout = Workout.objects.create(template=workout_template, owner=request.user)
        last_workout_with_template = Workout.objects.filter(template=workout_template, owner=request.user).order_by('-created')[1]
        last_workout_with_template_sets = calculate_totals_for_workout(last_workout_with_template)[0]
        template_workout = Workout.objects.get(is_template=True, template=workout_template, owner=request.user)
        template_workout_sets = calculate_totals_for_workout(template_workout)[0]
        if last_workout_with_template.is_template or last_workout_with_template.created < workout_template.updated \
            or last_workout_with_template_sets != template_workout_sets:
            last_workout_exercises = WorkoutExercise.objects.filter(workout=template_workout, owner=request.user)
            for exercise in last_workout_exercises:
                last_workout_sets = Set.objects.filter(workout_exercise=exercise)
                new_workout_exercise = WorkoutExercise.objects.create(exercise=exercise.exercise, order=exercise.order,
                                                                      workout=new_workout, owner=request.user)
                for set in last_workout_sets:
                    new_set = Set.objects.create(workout_exercise=new_workout_exercise, load=0,
                                                 repetitions=set.repetitions, order=set.order, owner=request.user)
        else:
            last_workout_exercises = WorkoutExercise.objects.filter(workout=last_workout_with_template)
            for exercise in last_workout_exercises:
                last_workout_sets = Set.objects.filter(workout_exercise=exercise, owner=request.user)
                new_workout_exercise = WorkoutExercise.objects.create(exercise=exercise.exercise, order=exercise.order,
                                                                      workout=new_workout, owner=request.user)
                for set in last_workout_sets:
                    new_set = Set.objects.create(workout_exercise=new_workout_exercise, load=set.load,
                                                 repetitions=set.repetitions, order=set.order, owner=request.user)
        return redirect('edit_workout', workout_pk=new_workout.pk)

@login_required
def edit_workout(request, workout_pk):
    new_workout = Workout.objects.get(id=workout_pk, owner=request.user)
    workout_template = new_workout.template
    new_workout_exercises = WorkoutExercise.objects.filter(workout=new_workout, owner=request.user)
    SetWorkoutFormset = inlineformset_factory(WorkoutExercise, Set, form=SetFormWorkout, can_delete=True, extra=0)
    workout_dict = {}
    if request.method == 'GET':
        for exercise in new_workout_exercises:
            formset = SetWorkoutFormset(instance=exercise, prefix=exercise.exercise)
            workout_dict[exercise] = formset
        ctx = {
                   'workout_dict': workout_dict
                }
        return render(request, 'edit_workout.html', ctx)

    if request.method == 'POST':
        for exercise in new_workout_exercises:
            formset = SetWorkoutFormset(request.POST, instance=exercise, prefix=exercise.exercise)
            for index, form in enumerate(formset):
                if form.is_valid():
                    new_set = form.save(commit=False)
                    new_set.owner = request.user
                    new_set.save()
                if not form.cleaned_data.get('done'):
                    form.instance.delete()
            sets = Set.objects.filter(workout_exercise=exercise, owner=request.user)
            if not sets:
                exercise.delete()
        new_workout_exercises = WorkoutExercise.objects.filter(workout=new_workout, owner=request.user)
        if not new_workout_exercises:
            new_workout.delete()
            return redirect('/main')
        new_workout.finished = True
        new_workout.save()
        return redirect('workout_details', workout_pk=new_workout.pk)


class WorkoutDetails(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, workout_pk):
        workout = Workout.objects.get(id=workout_pk, owner=request.user)
        ctx = {
            'workout_dict': create_workout_display(workout),
            'workout': workout,
            'workout_totals': calculate_totals_for_workout(workout),
        }
        return render(request, 'workout_details.html', ctx)


class WorkoutList(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        workout_list = Workout.objects.filter(is_template=False, owner=request.user).order_by('-created')
        workout_dict = {}
        for workout in workout_list:
            workout_exercises = WorkoutExercise.objects.filter(workout=workout)
            workout_exercises_count = workout_exercises.count()
            workout_totals = calculate_totals_for_workout(workout)
            workout_dict[workout] = {'exercises': workout_exercises, 'exercise_count': workout_exercises_count, 'totals': workout_totals}
        ctx = {
            'workout_dict': workout_dict
        }

        return render(request, 'workout_list.html', ctx)


class DeleteWorkout(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, workout_pk):
        workout = Workout.objects.get(id=workout_pk)
        workout.delete()
        return redirect('workout_list')


class LandingPage(View):
    def get(self, request):
        return render(request, 'landing_page.html')


class Analytics(LoginRequiredMixin, View):

    def get(self, request):
        templates = WorkoutTemplate.objects.filter(owner=request.user)
        return render(request, 'analytics.html')


@api_view()
@permission_classes([IsAuthenticated])
def date_filter(request):
    date_from = request.query_params.get('date_from')
    if not date_from:
        date_from = request.user.date_joined
    date_to = request.query_params.get('date_to')
    if not date_to:
        date_to = datetime.date.today()
    template = request.query_params.get('template')
    all_workouts = Workout.objects.filter(is_template=False, owner=request.user, finished=True, created__gte=date_from, created__lte=date_to)
    labels = []
    dataset = []
    for workout in all_workouts:
        labels.append(workout.id)
        dataset.append(calculate_totals_for_workout(workout)[2])
    return Response({'labels': labels, 'dataset': dataset})





















                    

































