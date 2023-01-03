from django import forms
from WorkoutTracker.models import Exercise, Equipment, Muscle, Workout, WorkoutTemplate


class ExerciseForm(forms.ModelForm):
    equipment_needed = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Exercise
        fields = '__all__'


class WorkoutForTemplateForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['comments']


class WorkoutTemplateForm(forms.ModelForm):
    class Meta:
        model = WorkoutTemplate
        fields = ['name']




