from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd
from io import BytesIO
from django.core.mail import EmailMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('GetJobPostReport')
                # Fetch the results
                result = cursor.fetchall()
                # Convert the result to a Pandas DataFrame
                df = pd.DataFrame(result, columns=['id', 'job_title', 'company_name', 'employee_type', 'location', 
                                                   'experience', 'salary_range', 'no_of_vacancies', 'company_logo', 
                                                   'job_role', 'created_at', 'skill_set'])
                # Convert DataFrame to Excel
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)
                # Send email with the Excel file attached
                subject = 'Job Post Table Report'
                message = 'Please find the attached job post table report.'
                from_email = 'brochill547@gmail.com'
                recipient_list = ['brochill547@gmail.com']
                email = EmailMessage(subject, message, from_email, recipient_list)
                email.attach('job_post_report.xlsx', excel_buffer.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                email.send()
                self.stdout.write(self.style.SUCCESS('Job post table report sent successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
