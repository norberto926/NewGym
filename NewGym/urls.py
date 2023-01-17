"""NewGym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from WorkoutTracker.views import CreateExercise, CreateWorkoutTemplate, EditWorkoutTemplate, \
    AddExerciseToWorkoutTemplate, CreateSetForWorkoutExercise, CreateWorkoutPlan, WorkoutPlanList, EditWorkoutPlan

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_exercise', CreateExercise.as_view(), name='create_exercise'),
    path('create_workout_template', CreateWorkoutTemplate.as_view(), name='create_workout_template'),
    path('edit_workout_template/<workout_template_id>', EditWorkoutTemplate.as_view(), name="edit_workout_template"),
    path('add_exercise_to_workout_template', AddExerciseToWorkoutTemplate.as_view(), name='add_exercise_to_workout_template'),
    path('create_set/<int:workout_exercise_id>', CreateSetForWorkoutExercise.as_view(), name="create_set"),
    path('create_workout_plan', CreateWorkoutPlan.as_view(), name='create_workout_plan'),
    path('workout_plan_list', WorkoutPlanList.as_view(), name='workout_plan_list'),
    path('edit_workout_plan/<int:workout_plan_id>', EditWorkoutPlan.as_view(), name='edit_workout_plan'),
]
