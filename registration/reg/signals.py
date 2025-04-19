import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Participant, UserCode

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Participant)
def create_verification_code(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        UserCode.objects.create(participant=instance)
        logger.info(f"Код создан для {instance.email}")
    except Exception as e:
        logger.error(f"Ошибка создания кода: {str(e)}", exc_info=True)
        raise