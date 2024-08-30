from django.urls import path

from habits import views
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path("habits/", views.HabitList.as_view(), name="habit-list"),
    path("habits/<int:pk>/", views.HabitDetail.as_view(), name="habit-detail"),
]
