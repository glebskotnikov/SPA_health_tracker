from rest_framework import serializers

from habits.models import Habit

from .validators import (
    validate_connected_habit_and_reward,
    validate_connected_habit_nature,
    validate_habit_duration,
    validate_habit_periodicity,
    validate_pleasant_habit,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
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
        ]
        validators = [
            validate_connected_habit_and_reward,
            validate_habit_duration,
            validate_connected_habit_nature,
            validate_pleasant_habit,
            validate_habit_periodicity,
        ]
