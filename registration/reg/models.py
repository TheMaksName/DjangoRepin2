# models.py
import random
import secrets
import string
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



def generate_unique_code(length=8):
    """Генерирует уникальный код из букв и цифр"""
    code = secrets.token_hex(length // 2).upper()[:length]
    while UserCode.objects.filter(code=code).exists():
        code = secrets.token_hex(length // 2).upper()[:length]
    return code


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название команды")

    work_theme = models.CharField(
        max_length=255,
        verbose_name="Тема работы",
        help_text="Укажите тему работы вашей команды"
        default=""  # Или любое другое значение по умолчанию
    )
    
    work_link = models.URLField(
    max_length=500,
    verbose_name="Ссылка на работу",
    help_text="Укажите ссылку на работу (если есть)",
    default=""  # Или любое другое значение по умолчанию
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'Participant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_teams'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class Mentor(models.Model):
    """Модель для хранения информации о наставниках"""
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    position = models.CharField(max_length=100, verbose_name="Должность")

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+79991234567'"
    )
    phone = models.CharField(
        max_length=16,
        validators=[phone_regex],
        unique=True,
        verbose_name="Телефон наставника"
    )


    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.phone})"

    class Meta:
        verbose_name = "Наставник"
        verbose_name_plural = "Наставники"
        indexes = [
            models.Index(fields=['phone']),
        ]


class Participant(models.Model):
    """Основная модель участника"""
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")

    email = models.EmailField(unique=True, verbose_name="Email участника")
    school = models.CharField(max_length=200, verbose_name="Школа")

    mentor = models.ForeignKey(
        Mentor,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Наставник"
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Команда"
    )

    consent_file = models.FileField(upload_to='consents/', verbose_name="Согласие")
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        indexes = [
            models.Index(fields=['email']),
        ]


class UserCode(models.Model):
    """Модель для хранения кодов Telegram-верификации"""
    participant = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name='verification_code',
        verbose_name="Участник"
    )

    telegram_username = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Telegram username"
    )
    telegram_chat_id = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Chat ID"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Подтвержден")
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)


    code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_unique_code,
        editable=False,
    )
    def __str__(self):
        return f"Код {self.code} для {self.participant}"

    class Meta:
        verbose_name = "Код верификации"
        verbose_name_plural = "Коды верификации"
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['telegram_username']),
            models.Index(fields=['is_verified']),
        ]


# @receiver(post_save, sender=Participant)
# def create_verification_code(sender, instance, created, **kwargs):
#     """Создает код верификации при регистрации участника"""
#     if created:
#         UserCode.objects.create(participant=instance)
