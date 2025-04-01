from django.shortcuts import render
from http import HTTPStatus
from django.http import JsonResponse
from rest_framework.views import APIView
from django.http import Http404
from django.utils.text import slugify 

# Create your views here.
class Clase1(APIView):
    def get(self, request):
        pass
    