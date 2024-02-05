from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd
from io import BytesIO
from django.core.mail import EmailMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            con = connection.cursor()
            sql = """
            SELECT 
                p.user_id, p.registered_by, p.first_name, p.last_name,
                p.date_of_birth, p.gender, p.profile_picture, p.created_at, p.updated_at,
                a.street, a.city, a.state, a.country, a.pincode, a.address_type,
                e.sslc_school_name, e.sslc_start_year, e.sslc_end_year, e.sslc_percentage,
                e.hsc_school_name, e.hsc_start_year, e.hsc_end_year, e.hsc_percentage,
                c.college_name, c.start_year, c.end_year, c.percentage, c.department, c.degree, c.education_type,
                j.key_skills, j.department, j.industry, j.preferred_locations,
                d.company_name, d.years_of_experience, d.job_role, d.skills,
                r.employment_status, r.resume
            FROM personal_details p
            LEFT JOIN address a ON a.user_id = p.user_id
            LEFT JOIN education_details e ON e.user_id = p.user_id
            LEFT JOIN college_details c ON c.user_id = p.user_id
            LEFT JOIN resume_details r ON r.user_id = p.user_id
            LEFT JOIN job_preferences j ON j.user_id = p.user_id
            LEFT JOIN professional_details d ON d.user_id = p.user_id;
            """
            con.execute(sql)
            result = con.fetchall()
            # Convert the result to a Pandas DataFrame
            df_merged = pd.DataFrame(result, columns=['user_id', 'registered_by', 'first_name',
                                                      'last_name', 'date_of_birth', 'gender', 'profile_picture', 'created_at', 'updated_at',
                                                      'street', 'city', 'state', 'country', 'pincode', 'address_type',
                                                      'sslc_school_name', 'sslc_start_year', 'sslc_end_year', 'sslc_percentage',
                                                      'hsc_school_name', 'hsc_start_year', 'hsc_end_year', 'hsc_percentage',
                                                      'college_name', 'start_year', 'end_year', 'percentage', 'department', 'degree', 'education_type',
                                                      'key_skills', 'department', 'industry', 'preferred_locations',
                                                      'company_name', 'years_of_experience', 'job_role', 'skills',
                                                      'employment_status', 'resume'])
            # Convert DataFrame to Excel
            excel_buffer = BytesIO()
            df_merged.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)

            # Send email with the Excel file attached
            subject = 'User Data Table Report'
            message = 'Please find the attached User Data table report.'
            from_email = 'brochill547@gmail.com'
            recipient_list = ['brochill547@gmail.com']

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach('user_data_report.xlsx', excel_buffer.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()

            self.stderr.write(self.style.SUCCESS('User data report sent successfully.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
