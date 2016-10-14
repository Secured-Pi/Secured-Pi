from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from .forms import PhotoForm
from .models import Photo
from django.views.decorators.csrf import csrf_exempt
from securedpi_facerec.facial_recognition import facial_recognition


@login_required
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if request.POST['start_training']:
            facial_recognition.train_recognizer()
        else:
            f = request.FILES['webcam']
            f.name = "{}-{}-adasda".format('member', request.user.pk)
            new_file = Photo(user=request.user, image=f)
            new_file.save()
            return JsonResponse({})
    return render(request, 'securedpi_facerec/training.html')
