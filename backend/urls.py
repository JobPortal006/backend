from django.urls import path
from data import views
from data.User_details import signup,login,forget_password,create_account_user
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup.signup),
    path('login/',login.login),
    path('loginWithOTP/',login.loginWithOTP),
    path('forgetpassword/',forget_password.forgetpassword),
    path('updatepassword/',forget_password.updatepassword),
    path('userRegister/', create_account_user.user_register.as_view()),
    path('upload-image/', views.ImageUploadView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)