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
from django.urls import path, include
from WorkoutTracker.views import CreateExercise, CreateWorkoutTemplate, MainPageView, edit_workout_template, \
    WorkoutTemplateList, ExerciseList, AddExercise, DeleteExercise, CreateWorkout, edit_workout, ArchiveTemplate, \
    WorkoutDetails, WorkoutList, CreateUser, DeleteWorkout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('create_exercise', CreateExercise.as_view(), name='create_exercise'),
    path('create_workout_template', CreateWorkoutTemplate.as_view(), name='create_workout_template'),
    path('edit_workout/<workout_pk>', edit_workout, name='edit_workout'),
    path('main/', MainPageView.as_view(), name='main_page'),
    path('edit_workout_template/<int:workout_template_pk>', edit_workout_template, name='edit_workout_template'),
    path('workout_template_list', WorkoutTemplateList.as_view(), name='workout_template_list'),
    path('exercise_list', ExerciseList.as_view(), name='exercise_list'),
    path('add_exercise/<int:workout_template_pk>', AddExercise.as_view(), name='add_exercise'),
    path('delete_exercise/<int:workout_template_pk>/<int:workout_exercise_pk>', DeleteExercise.as_view(), name='delete_exercise'),
    path('create_workout', CreateWorkout.as_view(), name='create_workout'),
    path('archive_template/<int:workout_template_pk>', ArchiveTemplate.as_view(), name='archive_template'),
    path('workout_details/<int:workout_pk>', WorkoutDetails.as_view(), name='workout_details'),
    path('workout_list', WorkoutList.as_view(), name='workout_list'),
    path('sign_up', CreateUser.as_view(), name='sign_up'),
    path('delete_workout/<int:workout_pk>', DeleteWorkout.as_view(), name='delete_workout')
]
