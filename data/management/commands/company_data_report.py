from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd
from io import BytesIO
from django.core.mail import EmailMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:

                # Your raw SQL query
                # sql = "CALL GetJobPostReport()"
                # cursor.execute(sql)
                cursor.callproc('GetEmployeerRegister')
                # Fetch the results
                result = cursor.fetchall()

                # Convert the result to a Pandas DataFrame
                df = pd.DataFrame(result, columns=['id','employee_id', 'company_logo', 'company_name', 'company_industry', 'company_description', 
                                                   'no_of_employees', 'company_website_link', 'contact_person_name', 'contact_person_position', 
                                                   'street', 'city', 'state','country', 'pincode', 'address_type','email','mobile_number'])

                # Convert DataFrame to Excel
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)

                # Send email with the Excel file attached
                subject = 'Company Details Table Report'
                message = 'Please find the attached Company details table report.'
                from_email = 'brochill547@gmail.com'
                recipient_list = ['brochill547@gmail.com']

                email = EmailMessage(subject, message, from_email, recipient_list)
                email.attach('company_details_report.xlsx', excel_buffer.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                email.send()

                self.stdout.write(self.style.SUCCESS('Company details table report sent successfully.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
