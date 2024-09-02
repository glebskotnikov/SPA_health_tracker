import datetime
from unittest.mock import patch
from urllib.parse import urlparse

import requests_mock
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from config.settings import TELEGRAM_TOKEN, TELEGRAM_URL
from habits.services import send_telegram_message
from habits.validators import (
    validate_connected_habit_and_reward,
    validate_connected_habit_nature,
    validate_habit_duration,
    validate_habit_periodicity,
    validate_pleasant_habit,
)
from users.models import User

from .models import Habit
from .tasks import send_reminders


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.client.force_authenticate(user=self.user)

    def create_habit(
            self,
            action="Drink water",
            location="Kitchen",
            time="09:00",
            is_pleasant=True,
            periodicity=1,
            reward="",
            duration=60,
            is_public=False,
    ):
        return Habit.objects.create(
            user=self.user,
            location=location,
            time=time,
            action=action,
            is_pleasant=is_pleasant,
            periodicity=periodicity,
            reward=reward,
            duration=duration,
            is_public=is_public,
        )

    def test_create_habit(self):
        """Habit creation test."""

        url = reverse("habits:habit-list")

        data = {
            "user": self.user.id,
            "location": "Kitchen",
            "time": "09:00",
            "action": "Drink water",
            "is_pleasant": True,
            "periodicity": 1,
            "reward": "",
            "duration": 60,
            "is_public": False,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, "Drink water")

    def test_get_habits_list(self):
        """The test of getting a list of habits"""

        self.create_habit()
        url = reverse("habits:habit-list")
        response = self.client.get(url, format="json")

        # Now we can make our assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit_names = [habit["action"] for habit in response.data["results"]]
        self.assertIn("Drink water", habit_names)
        self.assertEqual(response.data["results"][0]["action"], "Drink water")

    def test_update_habit(self):
        """Habit update test."""

        habit = self.create_habit()
        url = reverse("habits:habit-detail", kwargs={"pk": habit.id})
        data = {
            "user": self.user.id,
            "location": "Living room",
            "time": "10:00",
            "action": "Read a book",
            "is_pleasant": False,
            "periodicity": 2,
            "reward": "A cup of tea",
            "duration": 120,
            "is_public": True,
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Read a book")
        self.assertEqual(habit.location, "Living room")

    def test_delete_habit(self):
        """Habit delete test."""

        habit = self.create_habit()
        self.assertEqual(Habit.objects.count(), 1)

        url = reverse("habits:habit-detail", kwargs={"pk": habit.id})
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_retrieve(self):
        """Habit retrieve test."""

        habit = self.create_habit()
        url = reverse("habits:habit-detail", kwargs={"pk": habit.id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Drink water")
        self.assertEqual(response.data["location"], "Kitchen")

    def test_create_habit_with_related_habit(self):
        """Habit creation with related habit test."""

        related_habit = self.create_habit(
            action="Morning run", location="Park"
        )
        url = reverse("habits:habit-list")

        data = {
            "user": self.user.id,
            "location": "Kitchen",
            "time": "09:00",
            "action": "Drink water",
            "is_pleasant": False,
            "periodicity": 1,
            "reward": "",
            "duration": 60,
            "is_public": False,
            "related_habit": related_habit.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        created_habit = Habit.objects.order_by("-id").first()
        self.assertEqual(created_habit.related_habit, related_habit)

    def test_create_public_habit(self):
        """Public habit creation test."""

        url = reverse("habits:habit-list")

        data = {
            "user": self.user.id,
            "location": "Kitchen",
            "time": "09:00",
            "action": "Drink water",
            "is_pleasant": True,
            "periodicity": 1,
            "reward": "",
            "duration": 60,
            "is_public": True,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.get()
        self.assertEqual(habit.is_public, True)


class TestValidators(TestCase):
    # test for validate_connected_habit_and_reward
    def test_validate_connected_habit_and_reward_both_present(self):
        with self.assertRaises(ValidationError):
            validate_connected_habit_and_reward(
                {"related_habit": "Read book", "reward": "Watch TV"}
            )

    def test_validate_connected_habit_and_reward_one_present(self):
        try:
            validate_connected_habit_and_reward({"related_habit": "Read book"})
            validate_connected_habit_and_reward({"reward": "Watch TV"})
        except ValidationError:
            self.fail(
                "validate_connected_habit_and_reward raised "
                "ValidationError unexpectedly!"
            )

    # test for validate_habit_duration
    def test_validate_habit_duration_greater_than_120(self):
        with self.assertRaises(ValidationError):
            validate_habit_duration({"duration": 121})

    def test_validate_habit_duration_less_than_or_equal_to_120(self):
        try:
            validate_habit_duration({"duration": 120})
            validate_habit_duration({"duration": 119})
        except ValidationError:
            self.fail(
                "validate_habit_duration raised ValidationError unexpectedly!"
            )

    # test for validate_connected_habit_nature
    def test_validate_connected_habit_nature_unpleasant_habit(self):
        habit = Habit()
        habit.is_pleasant = False
        with self.assertRaises(ValidationError):
            validate_connected_habit_nature({"related_habit": habit})

    def test_validate_connected_habit_nature_pleasant_habit(self):
        habit = Habit()
        habit.is_pleasant = True
        try:
            validate_connected_habit_nature({"related_habit": habit})
        except ValidationError:
            self.fail(
                "validate_connected_habit_nature raised "
                "ValidationError unexpectedly!"
            )

    # test for validate_pleasant_habit
    def test_validate_pleasant_habit_with_reward_or_related_habit(self):
        with self.assertRaises(ValidationError):
            validate_pleasant_habit(
                {"is_pleasant": True, "reward": "Watch TV"}
            )
            validate_pleasant_habit(
                {"is_pleasant": True, "related_habit": "Read book"}
            )

    def test_validate_pleasant_habit_no_reward_no_related_habit(self):
        try:
            validate_pleasant_habit({"is_pleasant": True})
        except ValidationError:
            self.fail(
                "validate_pleasant_habit raised ValidationError unexpectedly!"
            )

    # test for validate_habit_periodicity
    def test_validate_habit_periodicity_less_than_1_or_greater_than_7(self):
        with self.assertRaises(ValidationError):
            validate_habit_periodicity({"periodicity": 0})
            validate_habit_periodicity({"periodicity": 8})

    def test_validate_habit_periodicity_between_1_and_7(self):
        try:
            validate_habit_periodicity({"periodicity": 1})
            validate_habit_periodicity({"periodicity": 7})
        except ValidationError:
            self.fail(
                "validate_habit_periodicity raised "
                "ValidationError unexpectedly!"
            )


class ServicesTestCase(TestCase):
    def test_send_telegram_message(self):
        chat_id = "chat_id"
        message = "message"

        url = f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage"

        with requests_mock.Mocker(real_http=True) as m:
            m.get(url, json={"ok": True})
            send_telegram_message(chat_id, message)

            assert m.called
            assert m.call_count == 1
            parsed_actual_url = urlparse(m.last_request.url)._replace(
                query=None
            )
            assert parsed_actual_url.geturl() == url


@override_settings(CELERY_ALWAYS_EAGER=True)
class TasksTestCase(TestCase):
    @patch("habits.tasks.send_telegram_message")
    def test_send_reminders(self, send_telegram_message_mock):
        now_time = timezone.now()
        habit_time = datetime.time(hour=now_time.hour, minute=now_time.minute)

        with timezone.override("UTC"):
            user = User.objects.create(email="email", tg_chat_id="tg_chat_id")
            Habit.objects.create(
                time=habit_time,
                user=user,
                action="action",
                is_pleasant=True,
                duration=60,
            )

            send_reminders()

            send_telegram_message_mock.assert_called_once_with(
                chat_id="tg_chat_id",
                message="Time for your habit: action",
            )
