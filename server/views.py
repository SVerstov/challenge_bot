import json
import telebot
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tgbot.utils import Bot



@csrf_exempt
def telegram_callback(request):
    # data = json.loads(request.body)
    #     # dispatch(data)
    #     # return JsonResponse({})

    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        Bot.process_new_updates([update])

        return HttpResponse("")
    else:
        raise PermissionDenied


