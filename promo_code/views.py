from django.shortcuts import render
from django.http import JsonResponse

def validate(request):
    return JsonResponse({
        'name': 'Jorge',
        'last_name': 'Falcón',
    })
