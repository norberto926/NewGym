import django_filters
from .models import Exercise, Equipment
from django import forms


class ExerciseFilter(django_filters.FilterSet):

    equipment_needed = django_filters.ModelMultipleChoiceFilter(queryset=Equipment.objects.all(),
                                                                widget=forms.CheckboxSelectMultiple())
    class Meta:

        model = Exercise
        fields = {'name': ['contains'], 'main_muscle_group': ['exact'], 'equipment_needed': ['exact']}