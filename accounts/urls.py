from . import views
from django.urls import path

app_name='accounts'

urlpatterns=[
    path('login',views.login_user,name="login"),
    path('logout',views.logout_user,name="logout"),
    path('signup',views.signup_user,name="signup"),
]
