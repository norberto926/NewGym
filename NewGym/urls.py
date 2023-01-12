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
from WorkoutTracker.views import AddNewExerciseView, AddNewWorkoutTemplateView, EditWorkoutTemplateView, \
    AddExerciseToWorkoutTemplate, CreateWsetforWorkoutTemplate, CreateWorkoutPlan, WorkoutPlanList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_new_exercise', AddNewExerciseView.as_view()),
    path('new_workout_template', AddNewWorkoutTemplateView.as_view()),
    path('edit_workout_template/<workout_template_id>', EditWorkoutTemplateView.as_view(), name="edit_workout_template"),
    path('add_exercise_to_workout_template', AddExerciseToWorkoutTemplate.as_view()),
    path('create_set/<exercise_id>', CreateWsetforWorkoutTemplate.as_view(), name="create_set"),
    path('create_workout_plan', CreateWorkoutPlan.as_view()),
    path('workout_plan_list', WorkoutPlanList.as_view(), name='workout_plan_list'),
]
