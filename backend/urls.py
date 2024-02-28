from django.urls import path
from data.Account_creation import signup,login,forget_password
from data.Account_creation.User_account import get_user_account,update_user_account,user_account
from data.Account_creation.Employeer_account import employeer_account, get_employeer_account,update_employeer_account
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from data.Job import post_job, search_jobs,job_details,employer_post_jobs,job_details_by_companyName,job_details_by_employeeType,update_job,delete_job,job_filtering,apply_job

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup.signup,name='signup'),
    path('login/',login.login,name='login'),
    path('loginWithOTP/',login.loginWithOTP,name='loginWithOTP'),
    path('forgetpassword/',forget_password.forgetpassword,name='forgetpassword'),
    path('updatepassword/',forget_password.updatepassword,name='updatepassword'),
    path('userRegister/', user_account.user_register.as_view(),name='userRegister'),
    path('employerRegister/', employeer_account.employer_register.as_view(),name='employeerRegister'),
    path('get_user_details/', get_user_account.get_user_details),
    path('update_user_details/', update_user_account.update_user_details),
    path('get_user_details_view/', get_user_account.get_user_details_view),
    path('get_employeer_details/', get_employeer_account.get_employeer_details),
    path('update_employeer_details/', update_employeer_account.update_employee_details),

    # JOB POST ---- APIs 
    path('job_post/',post_job.post_jobs),
    path('location/',post_job.locations),
    path('experience/',post_job.experience),
    path('company_name/',post_job.company_name),
    path('job_role/',post_job.job_role),
    path('employment_type/',post_job.employment_type),   
    path('skill_set/',post_job.skill_set),
    path('search_jobs/',search_jobs.search_job),
    path('job_details/',job_details.job_details),
    path('get_view_jobs/',search_jobs.get_view_jobs),
    path('get_job_details/',job_details.get_job_details),
    path('employeer_post_jobs/',employer_post_jobs.employeer_post_jobs),
    path('employeer_post_jobs_view/',employer_post_jobs.employer_post_jobs_view),
    path('job_details_by_companyName/',job_details_by_companyName.job_details_by_companyName),
    path('job_details_by_companyName_view/',job_details_by_companyName.job_details_by_companyName_view),
    path('job_details_by_employeeType/',job_details_by_employeeType.job_details_by_employeeType),
    path('job_details_by_employeeType_view/',job_details_by_employeeType.job_details_by_employeeType_view),
    path('apply_job/',apply_job.apply_job),


    path('update_job/',update_job.update_jobs),
    path('delete_job/',delete_job.delete_jobPost),
    path('filter_singleValue/',job_filtering.filter),
]
  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)