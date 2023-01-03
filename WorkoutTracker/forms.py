from django import forms
from WorkoutTracker.models import Exercise, Equipment, Muscle

# Equipment list for ExerciseForm equipment_needed choices list
# equipment = Equipment.objects.all()
# equipment_list = []
# for element in equipment:
#     equipment_list.append((element.id, element.name))

# Muscle list for ExerciseForm main_muscles_group choices list

# muscles = Muscle.objects.all()
# muscles_list = []
# for element in muscles:
#     muscles_list.append((element.id, element.name))


# class ExerciseForm(forms.Form):
#     name = forms.CharField(max_length=255, label="Exercise name")
#     description = forms.CharField(widget=forms.Textarea())
#     equipment_needed = forms.ChoiceField(choices=equipment_list, label="Equipment needed")
#     main_muscle_group = forms.ChoiceField(choices=muscles_list, label="Main muscle group")


class ExerciseForm(forms.ModelForm):
    equipment_needed = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Exercise
        fields = '__all__'



