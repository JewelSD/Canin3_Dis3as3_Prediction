from django.urls import path
from website import views
from appoint import views as appo
from chat import views as chati
from myvideo import views as vid

urlpatterns = [
    path('', views.signup, name=""),
    path('patientappo', appo.patientappo, name="patientappo"),
    path('docappo', appo.docappo, name="docappo"),
    path('docstatus', appo.docstatus, name="docstatus"),
    path('login/', views.loginn, name="login"),
    path('home', views.signup, name="home"),
    path('signup', views.signup, name="signup"),
    path('vetlogin/', views.vetloginn, name="vetlogin"),
    path('userprofile', views.userprofile, name="userprofile"),
    path('vetprofile', views.vetprofile, name="vetprofile"),
    path('predict', views.predict, name="predict"),
    path('skinpredict', views.skinpredict, name="skinpredict"),
    path('logout', views.user_logout, name="logout"),
    path('fetch_details/', appo.fetch_details, name='fetch_details'),
    path('delete_appointment/<int:appointment_id>',
         appo.delete_appointment, name='delete_appointment'),
    path('sample', views.sample, name="sample"),
    path('home1', chati.home1, name='home1'),
    path('<str:room>/', chati.room, name='room'),
    path('checkview', chati.checkview, name='checkview'),
    path('send', chati.send, name='send'),
    path('getMessages/<str:room>/', chati.getMessages, name='getMessages'),
    path('video', vid.video, name='videocall'),
    path('submit', vid.sub, name="submit"),
    path('joinvideo', appo.joinroom, name='joinvideo'),



]
