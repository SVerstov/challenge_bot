import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from telegram_bot.dispatcher import dispatch

@csrf_exempt
def telegram_callback(request):
    data = json.loads(request.body)
    dispatch(data)
    return JsonResponse({})

