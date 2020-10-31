from . import views
from django.urls import path

app_name='frontend'
urlpatterns=[
    path('',views.home,name="home"),
]
