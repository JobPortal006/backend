from django.core.management.base import BaseCommand
import pandas as pd
from io import BytesIO
from data.message import create_session
from django.core.mail import EmailMessage
from data.Tables.table import Signup, PersonalDetails, Address, EducationDetails, CollegeDetails, ProfessionalDetails, JobPreferences, ResumeDetails

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            session = create_session()
            # Querying data from the database
            query = session.query(Signup, PersonalDetails, Address, EducationDetails, CollegeDetails, ProfessionalDetails, JobPreferences, ResumeDetails).\
                join(PersonalDetails, Signup.id == PersonalDetails.user_id).\
                join(Address, Signup.id == Address.user_id).\
                join(EducationDetails, Signup.id == EducationDetails.user_id).\
                join(CollegeDetails, Signup.id == CollegeDetails.user_id).\
                join(ProfessionalDetails, Signup.id == ProfessionalDetails.user_id).\
                join(JobPreferences, Signup.id == JobPreferences.user_id).\
                join(ResumeDetails, Signup.id == ResumeDetails.user_id).\
                all()

            # Creating a DataFrame from the query result
            data = []
            user_ids = set()
            for result in query:
                signup, personal, address, education, college, professional, job_pref, resume = result
                # Initialize dictionary to hold professional details
                user_id = PersonalDetails.user_id
                # Check if the user ID is encountered before
                if user_id in user_ids:
                    continue  # Skip adding this user entry
                else:
                    user_ids.add(user_id)  # Add the user ID to encountered set
                professional_details = {}
                
                # Iterate over professional details and store them in the dictionary
                for i, prof_detail in enumerate(signup.professional_details, start=1):
                    professional_details[f'Company Name {i}'] = prof_detail.company_name
                    professional_details[f'Years of Experience {i}'] = prof_detail.years_of_experience
                    professional_details[f'Job Role {i}'] = prof_detail.job_role
                    professional_details[f'Skills {i}'] = prof_detail.skills
                data.append({
                    'Signup ID': signup.id,
                    'Signup By': signup.signup_by,
                    'Email': signup.email,
                    'Mobile Number': signup.mobile_number,
                    'First Name': personal.first_name,
                    'Last Name': personal.last_name,
                    'Date of Birth': personal.date_of_birth,
                    'Gender': personal.gender,
                    'Profile Picture Path': personal.profile_picture_path,
                    'SSLC Start Year': education.sslc_start_year,
                    'SSLC End Year': education.sslc_end_year,
                    'SSLC Percentage': education.sslc_percentage,
                    'HSC School Name': education.hsc_school_name,
                    'HSC Start Year': education.hsc_start_year,
                    'HSC End Year': education.hsc_end_year,
                    'HSC Percentage': education.hsc_percentage,
                    # 'Company Name': ', '.join(professional.company_name for professional in signup.professional_details),
                    # 'Years of Experience': ', '.join(str(professional.years_of_experience) for professional in signup.professional_details),
                    # 'Job Role': ', '.join(professional.job_role for professional in signup.professional_details),
                    # 'Skills': ', '.join(professional.skills for professional in signup.professional_details),
                    **professional_details,  # Unpack professional details dictionary
                    'Key Skills': job_pref.key_skills,
                    'Industry': job_pref.industry,
                    'Job Preferences Department': job_pref.department,
                    'Preferred Locations': job_pref.preferred_locations,
                    'Employment Status': resume.employment_status,
                    'Resume Path': resume.resume_path
                })
                # Check for address types and add them to the data if present
                if address.address_type in ['Current', 'Permanent']:
                    data[-1]['Address Type'] = address.address_type
                    data[-1]['Street'] = address.street
                    data[-1]['City'] = address.city
                    data[-1]['State'] = address.state
                    data[-1]['Country'] = address.country
                    data[-1]['Pincode'] = address.pincode
                # Check for education types and add them to the data if present
                if college.education_type in ['UG', 'Diploma']:
                    data[-1]['Education Type'] = college.education_type
                    data[-1]['College Name'] = college.college_name
                    data[-1]['College Start Year'] = college.start_year
                    data[-1]['College End Year'] = college.end_year
                    data[-1]['College Percentage'] = college.percentage
                    data[-1]['Department'] = college.department
                    data[-1]['Degree'] = college.degree
                if college.education_type in ['PG']:
                    data[-1]['Additional Education Type'] = college.education_type
                    data[-1]['Additional College Name'] = college.college_name
                    data[-1]['Additional College Start Year'] = college.start_year
                    data[-1]['Additional College End Year'] = college.end_year
                    data[-1]['Additional College Percentage'] = college.percentage
                    data[-1]['Additional Department'] = college.department
                    data[-1]['Additional Degree'] = college.degree

            df = pd.DataFrame(data)

            # Exporting DataFrame to Excel
            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)

            # Send email with the Excel file attached
            subject = 'Database Data Report'
            message = 'Please find the attached database data report.'
            from_email = 'brochill547@gmail.com'  # Update with your email
            recipient_list = ['brochill547@gmail.com']  # Update with recipient email(s)
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach('database_data_report.xlsx', excel_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()

            self.stdout.write(self.style.SUCCESS('Database data report sent successfully.'))
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))