from django.shortcuts import render
from django.http import HttpResponse
from .models import Message


def hello_world(request):
    return HttpResponse("Hello World!")


def hello_mysql(request):
    message = Message.objects.first() #fapp/models.pyから最初のメッセージを取得
    if message is None:
        message = {"text": "No messages found"}
    return render(request, 'hello_mysql.html', {"message": message})
