# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.db import connection
# import json
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
    
# @csrf_exempt
# def post_job(request):
#     try:
#         if request.method == 'POST':
#             data = json.loads(request.body)
#             jobDescription = data.get('jobDescription') 
#             jobTitle = data.get('jobTitle')
#             employmentType = data.get('employmentType')
#             keySkills = data.get('keySkills')
#             experience = data.get('experience')
#             salary = data.get('salary')
#             location = data.get('location')
#             noOfVacancies = data.get('noOfVacancies')
#             qualificationType = data.get('qualificationType')

#             if (
#                 jobDescription and jobTitle and employmentType and keySkills and
#                 experience and salary and location and noOfVacancies and qualificationType
#             ):
#                 # query.post_job(
#                 #     jobDescription, jobTitle, employmentType, keySkills,
#                 #     experience, salary, location, noOfVacancies, qualificationType
#                 # )
#                 subject = 'Post a Job'
#                 message_html = render_to_string('account.html')
#                 message_plain = strip_tags(message_html)
#                 from_email = 'brochill547@gmail.com'
#                 # recipient_list = [email]
#                 # send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
#                 # return response.handleSuccess("Job posted Successfully")
#             else:
#                 # return response.errorResponse("Invalid input data")
#     except Exception as e:
#         # return response.serverErrorResponse("Server error")
