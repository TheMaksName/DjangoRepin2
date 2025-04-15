# models.py
import random
import string
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



def generate_unique_code(length=8):
    """Генерирует уникальный код из букв и цифр"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not UserCode.objects.filter(code=code).exists():
            return code

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название команды")
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

class Participant(models.Model):
    """Основная модель участника"""
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+79991234567'"
    )
    phone = models.CharField(
        max_length=16,
        validators=[phone_regex],
        unique=True,
        verbose_name="Телефон"
    )

    email = models.EmailField(unique=True, verbose_name="Email")
    school = models.CharField(max_length=200, verbose_name="Школа")
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Команда"
    )

    mentor_last_name = models.CharField(max_length=100, verbose_name="Фамилия наставника")
    mentor_first_name = models.CharField(max_length=100, verbose_name="Имя наставника")
    mentor_middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество наставника")
    mentor_position = models.CharField(max_length=100, verbose_name="Должность наставника")

    consent_file = models.FileField(upload_to='consents/', verbose_name="Согласие")
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        indexes = [
            models.Index(fields=['phone']),
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
    code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_unique_code,
        editable=False,
        verbose_name="Код верификации"
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





# admin.py
from django.contrib import admin


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone', 'school')
    search_fields = ('last_name', 'first_name', 'email', 'phone')


@admin.register(UserCode)
class UserCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'participant', 'is_verified', 'telegram_username')
    list_filter = ('is_verified',)
    search_fields = ('code', 'participant__last_name', 'telegram_username')



@receiver(post_save, sender=Participant)
def create_verification_code(sender, instance, created, **kwargs):
    """Создает код верификации при регистрации участника"""
    if created:
        UserCode.objects.create(participant=instance)