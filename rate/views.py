from django.shortcuts import render
from django.http import HttpResponse,Http404

# Create your views here.
def start (request):
    return HttpResponse (' start.html')