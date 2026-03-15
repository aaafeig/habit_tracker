from rest_framework.serializers import ValidationError


class HabitValidator:

    def __call__(self, attrs):

        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")
        duration = attrs.get("duration")
        frequency = attrs.get("frequency")
        is_pleasant = attrs.get("is_pleasant")

        # нельзя одновременно reward и related_habit
        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать reward и связанную привычку."
            )

        # длительность
        if duration and duration > 120:
            raise ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд."
            )

        # периодичность
        if frequency and frequency > 7:
            raise ValidationError(
                "Нельзя выполнять привычку реже одного раза в 7 дней."
            )

        # связанная привычка должна быть приятной
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # приятная привычка не может иметь reward или related_habit
        if is_pleasant and (reward or related_habit):
            raise ValidationError(
                "Приятная привычка не может иметь reward или связанную привычку."
            )
