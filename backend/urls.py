from django.urls import path
from data import views
from data.User_details import signup,login,forget_password
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup.signup),
    path('login/',login.login),
    path('forgetpassword/',forget_password.forgetpassword),
    path('updatepassword/',forget_password.updatepassword),
    path('user_register/', views.user_register),
]

