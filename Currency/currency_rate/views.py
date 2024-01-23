from datetime import datetime

from django.http import JsonResponse
from django.http import HttpResponse
import requests

from .models import Cost_of_currency

URL = 'https://api.exchangerate-api.com/v4/latest/USD'


def get_data():
    if Cost_of_currency.objects.count() == 0:
        return 'записей нет'
    elif Cost_of_currency.objects.count() < 11:
        previous = Cost_of_currency.objects.all()[1:]
    else:
        previous = Cost_of_currency.objects.all()[1:10]
    current = Cost_of_currency.objects.latest('id')
    return JsonResponse(
        {'актуальный курс': current, 'последние 10 запросов': previous}
    )


def save_current():
    try:
        data = requests.get(URL)
        usd_to_rub = data['rates']['RUB']
    except Exception as error:
        return HttpResponse(
            f'проблема с подключением к api. причина {error}',
            status=500
        )
    else:
        Cost_of_currency.objects.create(value=usd_to_rub)


def get_current_usd(request):
    timeout =  11 # '''datetime.now() - Cost_of_currency.objects.latest('date').date'''
    if timeout >= 10: # .total_seconds()
        save_current()
        return get_data()
    else:
        return HttpResponse('превышено количество запросов', status=429)
