# reg/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Participant, UserCode, generate_unique_code  # Импорт из текущего приложения

@receiver(post_save, sender=Participant)
def create_verification_code(sender, instance, created, **kwargs):
    """Создает или обновляет код верификации"""
    if created:
        UserCode.objects.get_or_create(
            participant=instance,
            defaults={
                'code': generate_unique_code()  # Ваша функция генерации кода
            }
        )