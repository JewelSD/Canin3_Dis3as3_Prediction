from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from appoint.models import appointment
from django.contrib import messages
# from django.http import HttpResponse

# Create your views here.


# def video(request):
#     if 'username' in request.session:
#         username = request.session.get('username')
#         return render(request, "videouser.html", {'user': username})

#     if 'vetusername' in request.session:
#         vetusername = request.session.get('vetusername')

#         return render(request, "video.html", {'user': vetusername})

def video(request):
    if 'username' in request.session:
        username = request.session.get('username')
        return render(request, "videouser.html", {'user': username})

    if 'vetusername' in request.session:
        vetusername = request.session.get('vetusername')
        # Retrieve the value of 'a' from the URL parameters
        a = request.GET.get('a', None)
        if request.method == "POST":
            roomid = request.POST['roomIDInput']
            appo = appointment.objects.get(id=a)
            appo.roomid = roomid
            appo.save()
        return render(request, "video.html", {'user': vetusername, 'a': a})


def sub(request):
    if 'vetusername' in request.session:
        vetusername = request.session.get('vetusername')
        # Retrieve the value of 'a' from the URL parameters
        a = request.GET.get('a', None)
        if request.method == "POST":
            a = request.POST['aid']
            roomid = request.POST['roomIDInput']
            appo = appointment.objects.get(id=a)
            appo.roomid = roomid
            appo.save()
            messages.error(request, "RoomID and ID Submitted Successfully")
        return render (request,"submit.html",{'a': a})
