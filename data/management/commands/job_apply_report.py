from django.core.management.base import BaseCommand
from io import BytesIO
from django.core.mail import EmailMessage
import pandas as pd
from data.message import create_session
from data.Account_creation.Tables.table import ApplyJob, AdditionalQueries, Signup, JobPost, ResumeDetails

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            session = create_session()

            # Query data from the database using SQLAlchemy
            query = (
                session.query(
                    ApplyJob,
                    AdditionalQueries,
                    Signup,
                    JobPost,
                    ResumeDetails
                )
                .outerjoin(AdditionalQueries, ApplyJob.job_id == AdditionalQueries.job_id)
                .join(Signup, ApplyJob.user_id == Signup.id)
                .join(JobPost, ApplyJob.job_id == JobPost.id)
                .join(ResumeDetails, ApplyJob.resume_id == ResumeDetails.id)
                .all()
            )

            # Creating a DataFrame from the query result
            data = []
            for apply_job, additional_queries, signup, job_post, resume_details in query:
                if additional_queries:
                    total_experience = additional_queries.total_experience
                    current_ctc = additional_queries.current_ctc
                    expected_ctc = additional_queries.expected_ctc
                    notice_period = additional_queries.notice_period
                else:
                    total_experience = current_ctc = expected_ctc = notice_period = None
                
                data.append({
                    'User ID': signup.id,
                    # 'User Name': f"{signup.first_name} {signup.last_name}",  # Include user name
                    'User Email': signup.email,
                    'Resume Path': resume_details.resume_path,
                    'Job ID': job_post.id,
                    'Total Experience': total_experience,
                    'Current CTC': current_ctc,
                    'Expected CTC': expected_ctc,
                    'Notice Period': notice_period
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
