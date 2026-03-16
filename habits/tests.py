from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from habits.models import Habit


User = get_user_model()


class HabitAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            username="test",
            password="12345",
            phone_number="+111111111"
        )

        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place="home",
            time="08:00:00",
            action="run",
            duration=60,
            frequency=1
        )

    def test_create_habit(self):

        data = {
            "place": "park",
            "time": "09:00:00",
            "action": "walk",
            "duration": 60,
            "frequency": 1
        }

        response = self.client.post("/habits/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)


    def test_get_habits_list(self):

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_habit(self):

        data = {
            "action": "running"
        }

        response = self.client.patch(
            f"/habits/{self.habit.id}/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.habit.refresh_from_db()

        self.assertEqual(self.habit.action, "running")


    def test_delete_habit(self):

        response = self.client.delete(
            f"/habits/{self.habit.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_public_habits(self):

        Habit.objects.create(
            user=self.user,
            place="gym",
            time="10:00:00",
            action="train",
            duration=60,
            frequency=1,
            is_public=True
        )

        response = self.client.get("/habits/public/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_cannot_edit_other_user_habit(self):

        other_user = User.objects.create_user(
            email="user2@test.com",
            username="user2",
            password="12345",
            phone_number = "+222222222"
        )

        habit = Habit.objects.create(
            user=other_user,
            place="home",
            time="07:00:00",
            action="meditate",
            duration=60,
            frequency=1
        )

        response = self.client.patch(
            f"/habits/{habit.id}/",
            {"action": "new_action"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


