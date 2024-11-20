from django.urls import path
from appoint import views
from website import views as webview
from myvideo import views as videoview

urlpatterns = [
    path('patientappo', views.patientappo, name="patientappointment"),
    path('login/', webview.loginn, name="login"),
    path('video', videoview.video, name="videocall"),
    path('submit', videoview.video, name="submitt"),
    path('joinvideo', views.joinroom, name="joinvideo"),
    path('userprofile', webview.userprofile, name="userprofile"),
    path('vetprofile', webview.vetprofile, name="vetprofile"),
    # path('video/<str:video_id>/', videoview.video, name='video'),
]
