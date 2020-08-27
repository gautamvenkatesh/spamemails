from django.shortcuts import render
from django.http import HttpResponse
from .tasks import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'emails/index.html')

def emails(request):
    info = get_reg_html()
    return JsonResponse(info, safe = False)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        deleter(name)
    return HttpResponse()