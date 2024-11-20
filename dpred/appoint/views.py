from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
# from django.http import HttpResponse
from django.contrib import messages, auth
from django.urls import reverse, include
from django.contrib.auth.models import User
from website import urls as webite_url
from website.models import veterinarian
from .models import appointment
from django.contrib.auth import authenticate, login, logout
import datetime
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, get_object_or_404
# views.py
from django.http import JsonResponse

from django.core.serializers import serialize
from django.http import JsonResponse
from .models import appointment
from myvideo.views import video


def fetch_details(request):
    user_id = request.session.get('id')
    appointments = appointment.objects.filter(user_id=user_id,)
    appointments_json = serialize('json', appointments)
    print(appointments_json)
    return JsonResponse(appointments_json, safe=False)


def patientappo(request):
    if 'username' in request.session:
        if 'id' in request.session:
            useid = request.session.get('id')
            current = appointment.objects.filter(user_id=useid)
            veterinarians = veterinarian.objects.all()
            appoin = appointment.objects.all()
            if request.method == "POST":
                name = request.POST['name']
                breed = request.POST['breed']
                age = request.POST['age']
                vet_id = request.POST['veterinarian']
                adate = request.POST['adate']
                phone = request.POST['phone']
                user_id = request.POST['user_id']
                desc = request.POST['desc']

                myuser = appointment.objects.create(
                    name=name, dog_breed=breed, age=age, vet_id=vet_id, date=adate, phone=phone, desc=desc, user_id=user_id)
                myuser.save()
                messages.error(request, "Appointment Sent Successfully")
                return redirect('patientappo')

        return render(request, 'patientappo.html', {'veterinarians': veterinarians, 'appoin': appoin, 'useid': useid, 'current': current})
    else:
        return redirect('login/')


def docappo(request):

    if 'vetusername' in request.session:
        if 'vet_id' in request.session:
            vet_id = request.session.get('vet_id')
            current = appointment.objects.filter(vet_id=vet_id, status=1)
            pend = appointment.objects.filter(vet_id=vet_id, status=0)
            appoin = appointment.objects.all()
            vet = veterinarian.objects.all()

            if request.method == "POST":
                if 'approve' in request.POST:
                    time = request.POST['time']
                    a = request.POST['a']
                    docdesc = request.POST['docdesc']
                    appo = appointment.objects.get(id=a)
                    appo.time = time
                    appo.doc_desc = docdesc
                    appo.status = 1
                    appo.save()
                elif 'reject' in request.POST:
                    time = request.POST['time']
                    a = request.POST['a']
                    docdesc = request.POST['docdesc']
                    appo = appointment.objects.get(id=a)
                    appo.time = datetime.time(0, 0)
                    appo.doc_desc = docdesc
                    appo.status = 2
                    appo.save()
                elif 'call' in request.POST:
                    a = request.POST['a']
            # Construct the URL dynamically with the parameter 'a'
                    redirect_url = reverse('videocall') + f'?a={a}'
                    return redirect(redirect_url)
            return render(request, 'docappo.html', {'appoin': appoin, 'vet': vet, 'current': current, 'pend': pend})
    else:
        return redirect('vetlogin')


def joinroom(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/video?roomID="+roomID)

    return render(request, 'join1.html', {})


@csrf_exempt  # This decorator allows the view to accept POST requests without CSRF token
def delete_appointment(request, appointment_id):
    appt = get_object_or_404(appointment, pk=appointment_id)
    appt.delete()
    return JsonResponse({'message': 'Appointment deleted successfully.'})


def docstatus(request):

    return render(request, 'docstatus.html', {})
