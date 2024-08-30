from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    location = models.CharField(max_length=100, verbose_name="location")
    time = models.TimeField(verbose_name="time")
    action = models.CharField(max_length=100, verbose_name="action")
    is_pleasant = models.BooleanField(verbose_name="pleasant")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, verbose_name="related habit"
    )
    periodicity = models.PositiveIntegerField(default=1, verbose_name="periodicity")
    reward = models.CharField(max_length=100, blank=True, verbose_name="reward")
    duration = models.PositiveIntegerField(verbose_name="duration")
    is_public = models.BooleanField(default=False, verbose_name="public")

    class Meta:
        verbose_name = "habit"
        verbose_name_plural = "habits"
