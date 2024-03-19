from django.core.management.base import BaseCommand
from django.db import transaction
from io import BytesIO
from django.core.mail import EmailMessage
import pandas as pd
from data.message import create_session
from data.Account_creation.Tables.table import JobPost, Location, EmployeeTypes, JobRole, SkillSetMapping, SkillSets, QualificationMapping, Qualification, LocationMapping, Signup, CompanyDetails

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            session = create_session()

            # Query data from the database using SQLAlchemy
            query = (
                session.query(
                    JobPost,
                    Location,
                    EmployeeTypes,
                    JobRole,
                    SkillSetMapping,
                    SkillSets,
                    QualificationMapping,
                    Qualification,
                    LocationMapping,
                    Signup,
                    CompanyDetails
                )
                .join(EmployeeTypes, JobPost.employee_type_id == EmployeeTypes.id)
                .join(JobRole, JobPost.job_role_id == JobRole.id)
                .join(SkillSetMapping, JobPost.id == SkillSetMapping.job_id)
                .join(SkillSets, SkillSetMapping.skill_id == SkillSets.id)
                .join(QualificationMapping, JobPost.id == QualificationMapping.job_id)
                .join(Qualification, QualificationMapping.qualification_id == Qualification.id)
                .join(LocationMapping, JobPost.id == LocationMapping.job_id)
                .join(Location, LocationMapping.location_id == Location.id)
                .join(Signup, JobPost.employee_id == Signup.id)
                .join(CompanyDetails, JobPost.company_id == CompanyDetails.id)
                .all()
            )

            # Creating a DataFrame from the query result
            data = []
            job_ids = set()  # Maintain a set of encountered job IDs
            for result in query:
                job_post, location, employee_type, job_role, _, skill_set, _, qualification, _, signup, company_details = result
                job_id = job_post.id
                # Check if the job ID is encountered before
                if job_id in job_ids:
                    continue  # Skip adding this job entry
                else:
                    job_ids.add(job_id)  # Add the job ID to encountered set
                
                # Query qualification
                qualifications = ", ".join([q.qualification for q in session.query(Qualification).join(QualificationMapping).filter(QualificationMapping.job_id == job_id)])

                # Query location
                locations = ", ".join([l.location for l in session.query(Location).join(LocationMapping).filter(LocationMapping.job_id == job_id)])

                # Query skill set
                skill_sets = ", ".join([s.skill_set for s in session.query(SkillSets).join(SkillSetMapping).filter(SkillSetMapping.job_id == job_id)])
                
                data.append({
                    'Job Id': job_id,
                    'Job Title': job_post.job_title,
                    'Company Name': company_details.company_name,
                    'Location': locations,
                    'Employee Type': employee_type.employee_type,
                    'Job Role': job_role.job_role,
                    'Experience': job_post.experience,
                    'Salary Range': job_post.salary_range,
                    'Qualification': qualifications,
                    'Skills': skill_sets,
                    'No. of Vacancies': job_post.no_of_vacancies,
                    'Additional Queries': job_post.additional_queries,
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
