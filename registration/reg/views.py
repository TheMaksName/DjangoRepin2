from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import models
import logging

# Настройка логгера для отслеживания отправки писем
logger = logging.getLogger(__name__)

def registration(request):
    return render(request, 'registration.html')

def registration_true(request):
    return HttpResponse('Все хорошо')
    # return render(request, 'ura.html')
    # if request.method != 'POST':
    #     return HttpResponse("Неверный метод запроса", status=405)

    # try:
    #     # Валидация обязательных полей
    #     required_fields = {
    #         'last_name': "Фамилия",
    #         'first_name': "Имя",
    #         'email': "Email",
    #         'school_name': "Название школы",
    #         'phone': "Телефон",
    #         'mentor_last_name': "Фамилия наставника",
    #         'mentor_first_name': "Имя наставника",
    #         'mentor_position': "Должность наставника"
    #     }

    #     errors = {}
    #     data = {}

    #     for field, name in required_fields.items():
    #         value = request.POST.get(field, '').strip()
    #         if not value:
    #             errors[field] = f"Поле '{name}' обязательно для заполнения"
    #         data[field] = value

    #     # Обработка команды
    #     team_option = request.POST.get('team')
    #     custom_team = request.POST.get('custom_team')
    #     print(1, team_option)
    #     print(2 ,request.POST.get('custom_team'))
    #     if team_option == 'custom':
    #         if not custom_team:
    #             errors['team'] = "Укажите название команды"
    #         team_name = custom_team
    #     elif not team_option:
    #         errors['team'] = "Выберите или укажите команду"
    #     else:
    #         team_name = team_option

    #     # Проверка файла согласия
    #     consent_file = request.FILES.get('document')
    #     if not consent_file:
    #         errors['consent_file'] = "Необходимо загрузить файл согласия"

    #     if errors:
    #         return JsonResponse({'success': False, 'errors': errors}, status=400)

    #     # Проверка уникальности email и телефона
    #     if models.Participant.objects.filter(email=data['email']).exists():
    #         return JsonResponse(
    #             {'success': False, 'errors': {'email': "Пользователь с таким email уже зарегистрирован"}},
    #             status=400
    #         )

    #     if models.Participant.objects.filter(phone=data['phone']).exists():
    #         return JsonResponse(
    #             {'success': False, 'errors': {'phone': "Пользователь с таким телефоном уже зарегистрирован"}},
    #             status=400
    #         )

    #     # Получаем или создаем команду
    #     team, created = models.Team.objects.get_or_create(
    #         name=team_name,
    #         defaults={'name': team_name}
    #     )

    #     # Создание участника
    #     try:
    #         participant = models.Participant.objects.create(
    #             last_name=data['last_name'],
    #             first_name=data['first_name'],
    #             middle_name=request.POST.get('middle_name', '').strip(),
    #             email=data['email'],
    #             school=data['school_name'],
    #             phone=data['phone'],
    #             mentor_last_name=data['mentor_last_name'],
    #             mentor_first_name=data['mentor_first_name'],
    #             mentor_middle_name=request.POST.get('mentor_middle_name', '').strip(),
    #             mentor_position=data['mentor_position'],
    #             team=team,
    #             consent_file=consent_file
    #         )

    #         # Если команда новая, связываем ее с создателем
    #         if created:
    #             team.created_by = participant
    #             team.save()

    #         # Код верификации создается автоматически через сигнал
    #         user_code = models.UserCode.objects.get(participant=participant)

    #     except Exception as e:
    #         logger.error(f"Ошибка создания участника: {str(e)}", exc_info=True)
    #         return JsonResponse(
    #             {'success': False, 'message': "Ошибка при создании учетной записи"},
    #             status=500
    #         )

    #     # Отправка письма с кодом
    #     try:
    #         html_message = render_to_string(
    #             'registration_email.html',
    #             {
    #                 'name': participant.first_name,
    #                 'code': user_code.code,
    #                 'team_name': team.name,
    #                 'event_name': "Название Вашего Мероприятия"
    #             }
    #         )

    #         send_mail(
    #             subject="Ваш код для участия",
    #             message=strip_tags(html_message),
    #             html_message=html_message,
    #             from_email="repin.bot@yandex.ru",
    #             recipient_list=[participant.email],
    #             fail_silently=False,
    #         )
    #         logger.info(f"Отправлен код {user_code.code} для {participant.email}")

    #     except Exception as e:
    #         logger.error(f"Ошибка отправки письма: {str(e)}", exc_info=True)
    #         # Можно добавить повторную попытку через Celery

    #     # Рендеринг страницы успешной регистрации
    #     return render(request, 'registration_success.html', {
    #         'message': f"Регистрация успешна! Код отправлен на {participant.email}",
    #         'team_name': team.name,
    #         'email': participant.email
    #     })

    # except Exception as e:
    #     logger.error(f"Неожиданная ошибка регистрации: {str(e)}", exc_info=True)
    #     return JsonResponse(
    #         {'success': False, 'message': "Произошла непредвиденная ошибка"},
    #         status=500
    #     )
