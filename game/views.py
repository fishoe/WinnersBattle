from django.shortcuts import render
from django.http import JsonResponse
from .models import Player
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request,'main.html')

@csrf_exempt
def sign(request):
    print(here)
    mId = request.POST["sign_name"]
    mPass = request.POST['sign_pswd']
    try :
        p = Player(name=mId, password=mPass)
        p.save()
    except IntegrityError:
        return JsonResponse({'stat':'failed'})
    else :
        return JsonResponse({'stat':'success'})