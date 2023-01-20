from django import forms
from WorkoutTracker.models import Exercise, Equipment, Muscle, Workout, WorkoutTemplate, Set, WorkoutPlan


class ExerciseForm(forms.ModelForm):
    equipment_needed = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Exercise
        fields = '__all__'


class WorkoutTemplateForm(forms.ModelForm):
    class Meta:
        model = WorkoutTemplate
        fields = ['name']


class AddExerciseForm(forms.Form):
    exercise = forms.ChoiceField(choices=Exercise.objects.all())


class SetFormWorkoutTemplate(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['repetitions']


class WorkoutPlanForm(forms.Form):
    name = forms.CharField(max_length=64)\

class CreateSetForWorkoutForm(forms.Form):
    ...














