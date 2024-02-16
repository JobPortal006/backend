from django.urls import path
from data.Account_creation import signup,login,forget_password,create_account_user,create_account_employeer
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from data.Job import post_job,view_jobs,job_details,employer_post_jobs,search_job

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup.signup,name='signup'),
    path('login/',login.login,name='login'),
    path('loginWithOTP/',login.loginWithOTP,name='loginWithOTP'),
    path('forgetpassword/',forget_password.forgetpassword,name='forgetpassword'),
    path('updatepassword/',forget_password.updatepassword,name='updatepassword'),
    path('userRegister/', create_account_user.user_register.as_view(),name='userRegister'),
    path('employerRegister/', create_account_employeer.employer_register.as_view(),name='employeerRegister'),
    
    # JOB POST ---- APIs 
    path('job_post/',post_job.post_jobs),
    path('location/',post_job.locations),
    path('experience/',post_job.experience),
    path('company_name/',post_job.company_name),
    path('job_role/',post_job.job_role),
    path('employment_type/',post_job.employment_type),   
    path('skill_set/',post_job.skill_set),
    path('view_jobs/',view_jobs.view_jobs),
    path('search_jobs/',search_job.search_job),
    path('job_details/',job_details.job_details),
    # path('get_view_jobs/',view_jobs.get_view_jobs),
    path('get_job_details/',job_details.get_job_details),
    path('employer_post_jobs/',employer_post_jobs.employer_post_jobs),
    path('employer_post_jobs_view/',employer_post_jobs.employer_post_jobs_view)
]
  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)