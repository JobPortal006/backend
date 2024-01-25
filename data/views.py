from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from data import query, response


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.db import connection
import os

@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('file')
        print(image)
        fs = FileSystemStorage()
        desired_location = r'D:\Django project\demo\Images'
        full_file_path = os.path.join(desired_location, image.name)
        print(desired_location,"------------------ ",full_file_path)
        
        with open(full_file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        filename = fs.save('images/' + image.name, image)

        saved_image_path = fs.url(filename)

        save_image_path(saved_image_path)

        return JsonResponse({'message': 'File uploaded successfully.'}, status=200)

def save_image_path(image_path):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO your_table_name (image_path) VALUES (%s)", (image_path,))
    connection.commit()
    cursor.close()
    connection.close()


@csrf_exempt
def user_register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            email = data.get('email')
            address = data.get('address')
            mobileNumber = data.get('mobileNumber')
            gender = data.get('gender')
            experience = data.get('experience')
            percentage10 = data.get('percentage10')
            educationType = data.get('educationType')
            percentage12 = data.get('percentage12')
            diplomaPercentage = data.get('diplomaPercentage')
            department = data.get('department')
            collegeName = data.get('collegeName')
            batchYear = data.get('batchYear')
            companyName = data.get('companyName')
            role = data.get('role')
            position = data.get('position')
            relocate = data.get('relocate')
            profilePicture = data.get('profilePicture')
            resume = data.get('resume')

            if (
                firstName != '' and lastName != '' and email != '' and address != '' and mobileNumber != '' and gender != '' and 
                experience != '' and percentage10 != '' and educationType != '' and department != '' and collegeName != '' and 
                batchYear != '' and companyName != '' and role != '' and position != '' and relocate != '' and profilePicture != '' and resume != ''
            ):
                query.user_account(
                    firstName, lastName, email, address, mobileNumber, gender, experience, percentage10, educationType,
                    percentage12, diplomaPercentage, department, collegeName,
                    batchYear, companyName, role, position, relocate,profilePicture, resume
                )

                subject = 'Account Creation'
                message_html = render_to_string('account.html', {'name': firstName})
                message_plain = strip_tags(message_html)
                from_email = 'brochill547@gmail.com'
                recipient_list = [email]
                send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)

                return response.handleSuccess("Account created Successfully")
            else:
                return response.errorResponse("Invalid input data")
    except Exception as e:
        print(str(e))
        return response.serverErrorResponse("Server error")
    
@csrf_exempt
def post_job(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            jobDescription = data.get('jobDescription')
            jobTitle = data.get('jobTitle')
            employmentType = data.get('employmentType')
            keySkills = data.get('keySkills')
            experience = data.get('experience')
            salary = data.get('salary')
            location = data.get('location')
            noOfVacancies = data.get('noOfVacancies')
            qualificationType = data.get('qualificationType')

            if (
                jobDescription and jobTitle and employmentType and keySkills and
                experience and salary and location and noOfVacancies and qualificationType
            ):
                query.post_job(
                    jobDescription, jobTitle, employmentType, keySkills,
                    experience, salary, location, noOfVacancies, qualificationType
                )
                subject = 'Post a Job'
                message_html = render_to_string('account.html')
                message_plain = strip_tags(message_html)
                from_email = 'brochill547@gmail.com'
                # recipient_list = [email]
                # send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                return response.handleSuccess("Job posted Successfully")
            else:
                return response.errorResponse("Invalid input data")
    except Exception as e:
        return response.serverErrorResponse("Server error")
