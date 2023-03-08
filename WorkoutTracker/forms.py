from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from WorkoutTracker.models import Exercise, Equipment, WorkoutTemplate, Set


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ExerciseForm(forms.ModelForm):
    equipment_needed = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple, blank=True, required=False)

    class Meta:
        model = Exercise
        fields = ['name', 'main_muscle_group', 'description']


class WorkoutTemplateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control text-light bg-secondary', 'style':'text-align:center;'}), label='')

    class Meta:
        model = WorkoutTemplate
        fields = ['name']


class AddExerciseForm(forms.Form):
    exercise = forms.ChoiceField(choices=Exercise.objects.all())


class SetFormWorkoutTemplate(forms.ModelForm):
    repetitions = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control text-light bg-secondary', 'style': 'text-align:center;'}), label='')

    class Meta:
        model = Set
        fields = ['repetitions']


class SetFormWorkout(forms.ModelForm):
    load = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control text-light bg-secondary', 'style': 'text-align:center;'}), label='')
    repetitions = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control text-light bg-secondary', 'style': 'text-align:center;'}), label='')
    done = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input text-light bg-secondary'}))

    class Meta:
        model = Set
        fields = ['repetitions', 'load', 'done']























