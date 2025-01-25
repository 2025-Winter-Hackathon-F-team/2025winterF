from django.shortcuts import render
from django.http import HttpResponse

def hello_world(requests):
    return HttpResponse("Hello World!")