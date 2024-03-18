from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import BytesIO
from django.core.mail import EmailMessage
from data.Account_creation.Tables.table import Signup, PersonalDetails, Address, EducationDetails, CollegeDetails, ProfessionalDetails, JobPreferences, ResumeDetails

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # Establishing connection to the database
            engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/jobportal')
            Session = sessionmaker(bind=engine)
            session = Session()

            # Querying data from the database
            query = session.query(Signup, PersonalDetails, Address, EducationDetails, CollegeDetails, ProfessionalDetails, JobPreferences, ResumeDetails).\
                join(PersonalDetails).\
                join(Address).\
                join(EducationDetails).\
                join(CollegeDetails).\
                join(ProfessionalDetails).\
                join(JobPreferences).\
                join(ResumeDetails).\
                all()

            # Creating a DataFrame from the query result
            data = []
            for result in query:
                signup, personal, address, education, college, professional, job_pref, resume = result
                # Initialize dictionary to hold professional details
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
                    # 'Street': address.street,
                    # 'City': address.city,
                    # 'State': address.state,
                    # 'Country': address.country,
                    # 'Pincode': address.pincode,
                    # 'Address Type': address.address_type,
                    # 'SSLC School Name': education.sslc_school_name,
                    'SSLC Start Year': education.sslc_start_year,
                    'SSLC End Year': education.sslc_end_year,
                    'SSLC Percentage': education.sslc_percentage,
                    'HSC School Name': education.hsc_school_name,
                    'HSC Start Year': education.hsc_start_year,
                    'HSC End Year': education.hsc_end_year,
                    'HSC Percentage': education.hsc_percentage,
                    # 'College Name': college.college_name,
                    # 'College Start Year': college.start_year,
                    # 'College End Year': college.end_year,
                    # 'College Percentage': college.percentage,
                    # 'Department': college.department,
                    # 'Degree': college.degree,
                    # 'Education Type': college.education_type,
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
                # Check for additional address types and add them to the data if present
                if address.address_type in ['Current', 'Permanent']:
                    data[-1]['Additional Address Type'] = address.address_type
                    data[-1]['Additional Street'] = address.street
                    data[-1]['Additional City'] = address.city
                    data[-1]['Additional State'] = address.state
                    data[-1]['Additional Country'] = address.country
                    data[-1]['Additional Pincode'] = address.pincode
                # Check for additional education types and add them to the data if present
                if education.education_type in ['UG', 'Diploma', 'PG']:
                    data[-1]['Additional Education Type'] = education.education_type
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
            from_email = 'your_email@example.com'  # Update with your email
            recipient_list = ['recipient@example.com']  # Update with recipient email(s)
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach('database_data_report.xlsx', excel_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()

            self.stdout.write(self.style.SUCCESS('Database data report sent successfully.'))
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))