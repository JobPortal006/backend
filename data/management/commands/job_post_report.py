from django.core.management.base import BaseCommand
from django.db import transaction
from io import BytesIO
from django.core.mail import EmailMessage
import pandas as pd
from data.message import create_session
from sqlalchemy import create_engine, func
from data.Account_creation.Tables.table import JobPost, Location, EmployeeTypes, JobRole, SkillSetMapping, SkillSets, QualificationMapping, Qualification, LocationMapping, Signup, CompanyDetails

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # Establishing connection to the database
            engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/jobportal')
            # Begin a transaction
            with transaction.atomic():
                session = create_session()
                # Query data from the database using SQLAlchemy
                query = (
                    session.query(JobPost, Location, EmployeeTypes, JobRole, SkillSetMapping, SkillSets, QualificationMapping, Qualification, LocationMapping, Signup, CompanyDetails)
                    .join(Location)
                    .join(EmployeeTypes)
                    .join(JobRole)
                    .join(SkillSetMapping)
                    .join(SkillSets)
                    .join(QualificationMapping)
                    .join(Qualification)
                    .join(LocationMapping)
                    .join(Signup)
                    .join(CompanyDetails)
                    .all()
                )
                
                # Creating a DataFrame from the query result
                data = []
                for result in query:
                    job_post, location, employee_type, job_role, _, _, _, _, _, signup, company_details = result
                    skill_sets = ', '.join(mapping.skill_set.skill_set for mapping in job_post.skill_set_mappings)
                    qualifications = ', '.join(mapping.qualification.qualification for mapping in job_post.qualification_mappings)
                    locations = ', '.join(mapping.location.location for mapping in job_post.location_mappings)

                    data.append({
                        'Job Title': job_post.job_title,
                        'Company Name': company_details.company_name,
                        'Location': locations,
                        'Employee Type': employee_type.employee_type,
                        'Job Role': job_role.job_role,
                        'Experience': job_post.experience,
                        'Salary Range': job_post.salary_range,
                        'No. of Vacancies': job_post.no_of_vacancies,
                        'Additional Queries': job_post.additional_queries,
                        'Employee': f"{signup.first_name} {signup.last_name}",
                        'Skill Sets': skill_sets,
                        'Qualifications': qualifications
                    })

                # Convert DataFrame to Excel
                df = pd.DataFrame(data)
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)

                # Send email with the Excel file attached
                subject = 'Job Post Report'
                message = 'Please find the attached job post report.'
                from_email = 'brochill547@gmail.com'  # Update with your email
                recipient_list = ['brochill547@gmail.com']  # Update with recipient email(s)
                email = EmailMessage(subject, message, from_email, recipient_list)
                email.attach('job_post_report.xlsx', excel_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                email.send()

                self.stdout.write(self.style.SUCCESS('Job post report sent successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
