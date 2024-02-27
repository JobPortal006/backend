from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd
from io import BytesIO
from django.core.mail import EmailMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            con = connection.cursor()
            # Retrieve data from the signup table
            sql = "SELECT * FROM signup"
            con.execute(sql)
            result = con.fetchall()
            # Convert the result to a Pandas DataFrame
            df = pd.DataFrame(result, columns=['id', 'signup_by', 'email', 'mobile_number', 'password', 'created_at', 'updated_at'])
            # Convert DataFrame to Excel
            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)
            # Send email with the Excel file attached
            subject = 'Signup Table Report'
            message = 'Please find the attached signup table report.'
            from_email = 'brochill547@gmail.com'
            recipient_list = ['brochill547@gmail.com']
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach('signup_report.xlsx', excel_buffer.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()
            self.stderr.write(self.style.SUCCESS('Signup table report sent successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))

