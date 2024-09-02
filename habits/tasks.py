from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_reminders():
    now = timezone.now()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
    for habit in habits:
        send_telegram_message(
            chat_id=habit.user.tg_chat_id,
            message=f"Time for your habit: {habit.action}",
        )
