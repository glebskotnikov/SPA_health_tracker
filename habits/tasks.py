from .services import send_telegram_message
from celery import shared_task
from .models import Habit
from django.utils import timezone


@shared_task
def send_reminders():
    now = timezone.now()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
    for habit in habits:
        send_telegram_message(chat_id=habit.user.tg_chat_id, message=f"Time for your habit: {habit.action}")
