from django.urls import path
from data import views
from data.User_details import signup,login,forget_password,create_account_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup.signup),
    path('login/',login.login),
    path('loginWithOTP/',login.loginWithOTP),
    path('forgetpassword/',forget_password.forgetpassword),
    path('updatepassword/',forget_password.updatepassword),
    path('userRegister/', create_account_user.user_register),
]

