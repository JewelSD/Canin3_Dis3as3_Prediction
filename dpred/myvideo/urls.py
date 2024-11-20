from django.urls import path
from myvideo import views
from website import views as webview

urlpatterns=[
    path('video',views.video,name="videocall"),
    path('submit',views.sub,name="submit"),
    path('vetprofile', webview.vetprofile, name="vetprofile"),
    path('userprofile', webview.userprofile, name="userprofile"),
    # path('video/<int>/', views.video, name='videocall'),
]