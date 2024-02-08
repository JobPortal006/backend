from django.urls import path
from data.Account_creation import signup,login,forget_password,create_account_user
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from data.Job import post_job 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup.signup,name='signup'),
    path('login/',login.login,name='login'),
    path('loginWithOTP/',login.loginWithOTP,name='loginWithOTP'),
    path('forgetpassword/',forget_password.forgetpassword,name='forgetpassword'),
    path('updatepassword/',forget_password.updatepassword,name='updatepassword'),
    path('userRegister/', create_account_user.user_register.as_view(),name='userRegister'),
    
    # JOB POST ---- APIs 
    path('job_post/',post_job.post_jobs),
    path('location/',post_job.locations),
    path('experience/',post_job.experience),
    
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)