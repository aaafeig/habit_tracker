from django.conf import settings
from django.db import models


class Habit(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits"
    )

    place = models.CharField(max_length=255)

    time = models.TimeField()

    action = models.CharField(max_length=255)

    is_pleasant = models.BooleanField(default=False)

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    frequency = models.PositiveIntegerField(
        default=1,
        help_text="периодичность в днях"
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    duration = models.PositiveIntegerField(
        help_text="время выполнения в секундах"
    )

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action
