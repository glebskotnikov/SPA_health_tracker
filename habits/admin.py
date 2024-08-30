from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "location",
        "time",
        "action",
        "is_pleasant",
        "related_habit",
        "periodicity",
        "reward",
        "duration",
        "is_public",
    )
