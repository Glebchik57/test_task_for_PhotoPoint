from datetime import datetime, timezone

from django.http import JsonResponse
from django.http import HttpResponse
import requests

from .models import Cost_of_currency

URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def make_data():
    '''Формирует json ответ'''
    if not Cost_of_currency.objects.all().exists():
        previous = []
    elif Cost_of_currency.objects.count() < 11:
        previous = list(Cost_of_currency.objects.values('value')[1:])
    else:
        previous = list(Cost_of_currency.objects.values('value')[1:10])
    current = Cost_of_currency.objects.latest('id').value
    return JsonResponse(
        {'current value': current, 'last values': previous}
    )


def save_rate():
    '''Запрашивает у API курс доллара и сохраняет его в базу'''
    try:
        data = requests.get(
            URL
        ).json()
        usd_to_rub = round(float(data['Valute']['USD']['Value']), 2)
    except Exception:
        raise
    else:
        Cost_of_currency.objects.create(value=usd_to_rub)


def current_usd(request):
    '''Основная логика работы сервиса'''
    exc = HttpResponse(
            'проблема с подключением к api',
            status=500
        )
    if Cost_of_currency.objects.all().exists():
        timeout = datetime.now(timezone.utc) - Cost_of_currency.objects.latest('date').date
        if timeout.total_seconds() >= 10:
            try:
                save_rate()
            except Exception:
                return exc
            else:
                return make_data()
        else:
            return HttpResponse('превышено количество запросов', status=429)
    else:
        try:
            save_rate()
        except Exception:
            return exc
        else:
            current = Cost_of_currency.objects.latest('id').value
            return JsonResponse({'value': current})
