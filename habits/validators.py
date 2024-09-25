from rest_framework.serializers import ValidationError


def validate_connected_habit_and_reward(data):
    if data.get("related_habit") and data.get("reward"):
        raise ValidationError(
            "Both connected habit and reward " "cannot be chosen at the same time."
        )


def validate_habit_duration(data):
    if data.get("duration", 0) > 120:
        raise ValidationError("Duration cannot be greater than 120 seconds.")


def validate_connected_habit_nature(data):
    related_habit = data.get("related_habit")
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError("Connected habit must be a pleasant one.")


def validate_pleasant_habit(data):
    if data.get("is_pleasant") and (data.get("reward") or data.get("related_habit")):
        raise ValidationError("Pleasant habit can not have reward or related habit.")


def validate_habit_periodicity(data):
    periodicity = data.get("periodicity")
    if periodicity < 1 or periodicity > 7:
        raise ValidationError(
            "Habit can not be performed less than once "
            "per 7 days or more than once per day."
        )
