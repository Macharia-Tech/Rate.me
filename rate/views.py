from django.shortcuts import render
from django.http import HttpResponse,Http404

# Create your views here.
def start (request):
    return HttpResponse (' Project Rator')

    except ValueError:
        #Raise 404 error when ValueError is thrown raise Http404() 