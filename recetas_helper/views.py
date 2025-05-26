from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404, HttpResponseRedirect

class Clase1(APIView):
    def get(self, request):
        pass
    
    