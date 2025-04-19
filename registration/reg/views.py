from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from background_task import background
from . import models
import logging

logger = logging.getLogger(__name__)

def registration(request):
    teams = models.Team.objects.all().order_by('name').values_list('name', flat=True)
    return render(request, 'registration.html', {'teams': teams})

def registration_true(request):
    if request.method != 'POST':
        return render(request, 'registration_error.html', {
            'error_message': "Неверный метод запроса"
        }, status=405)

    try:
        # Валидация обязательных полей
        required_fields = {
            'last_name': "Фамилия",
            'first_name': "Имя",
            'email': "Email",
            'school_name': "Название школы",
            'mentor_phone': "Телефон",
            'mentor_last_name': "Фамилия наставника",
            'mentor_first_name': "Имя наставника",
            'mentor_position': "Должность наставника"
        }

        errors = {}
        data = {}

        for field, name in required_fields.items():
            value = request.POST.get(field, '').strip()
            if not value:
                errors[field] = f"Поле '{name}' обязательно для заполнения"
            data[field] = value

        # Обработка команды
        team_option = request.POST.get('team')
        custom_team = request.POST.get('custom_team')

        if team_option == 'custom':
            if not custom_team:
                errors['team'] = "Укажите название команды"
            team_name = custom_team
        elif not team_option:
            errors['team'] = "Выберите или укажите команду"
        else:
            team_name = team_option

        # Проверка файла согласия
        consent_file = request.FILES.get('document')
        if not consent_file:
            errors['consent_file'] = "Необходимо загрузить файл согласия"

        if errors:
            return render(request, 'registration_error.html', {
                'errors': errors,
                'error_message': "Пожалуйста, исправьте ошибки в форме"
            }, status=400)

        # Проверка уникальности email
        if models.Participant.objects.filter(email=data['email']).exists():
            return render(request, 'registration_error.html', {
                'error_message': "Пользователь с таким email уже зарегистрирован"
            }, status=400)

        # Проверка уникальности телефона наставника
        mentor_phone = data['mentor_phone']
        if models.Mentor.objects.filter(phone=mentor_phone).exists():
            mentor = models.Mentor.objects.get(phone=mentor_phone)
            if (mentor.last_name != data['mentor_last_name'] or
                mentor.first_name != data['mentor_first_name']):
                return render(request, 'registration_error.html', {
                    'error_message': "Наставник с таким номером телефона уже существует, но с другими данными"
                }, status=400)

        mentor, created = models.Mentor.objects.get_or_create(
            phone=mentor_phone,
            defaults={
                'last_name': data['mentor_last_name'],
                'first_name': data['mentor_first_name'],
                'middle_name': request.POST.get('mentor_middle_name', '').strip(),
                'position': data['mentor_position'],
            }
        )

        # Получаем или создаем команду
        team, created = models.Team.objects.get_or_create(
            name=team_name,
            defaults={'name': team_name}
        )

        # Создание участника
        try:
            participant = models.Participant.objects.create(
                last_name=data['last_name'],
                first_name=data['first_name'],
                middle_name=request.POST.get('middle_name', '').strip(),
                email=data['email'],
                school=data['school_name'],
                mentor=mentor,
                team=team,
                consent_file=consent_file
            )

            logger.info(f"Участник создан: {participant.email}")

            if created:
                team.created_by = participant
                team.save()

            user_code = models.UserCode.objects.get(participant=participant)
            logger.info(f"Код создан: {user_code.code}")

            return render(request, 'registration_success.html', {
                'message': f"Регистрация успешна! Ваш код для входа: {user_code.code}",
            })

        except Exception as e:
            logger.error(f"Ошибка создания участника: {str(e)}", exc_info=True)
            return render(request, 'registration_error.html', {
                'error_message': "Ошибка при создании учетной записи"
            }, status=500)

    except Exception as e:
        logger.error(f"Неожиданная ошибка регистрации: {str(e)}", exc_info=True)
        return render(request, 'registration_error.html', {
            'error_message': "Произошла непредвиденная ошибка"
        }, status=500)