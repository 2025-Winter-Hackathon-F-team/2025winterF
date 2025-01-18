from django.shortcuts import render
from django.http import HttpResponse
from .models import Message

def hello_world(requests):
    return HttpResponse("Hello World!")

def hello_mysql(request):
    message = Message.objects.first() #最初のメッセージを取得
    return render(request, 'hello_mysql.html', {"message":message})