from django.core.management.base import BaseCommand
import pandas as pd
from io import BytesIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.Account_creation.Tables.table import Signup, CompanyDetails, Address
from django.core.mail import EmailMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # Establishing connection to the database
            engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/jobportal')
            Session = sessionmaker(bind=engine)
            session = Session()

            # Querying data from the CompanyDetails table
            query = session.query(CompanyDetails).all()

            # Creating a DataFrame from the query result
            data = []
            for company_detail in query:
                # Initialize list to hold address details
                addresses = []
                # Fetch all addresses associated with the current company detail
                for address in session.query(Address).filter(Address.user_id == company_detail.employee_id).all():
                    addresses.append({
                        'street': address.street,
                        'city': address.city,
                        'state': address.state,
                        'country': address.country,
                        'pincode': address.pincode,
                        'address_type': address.address_type
                    })
                data.append({
                    'id': company_detail.id,
                    'employee_id': company_detail.employee_id,
                    'company_name': company_detail.company_name,
                    'no_of_employees': company_detail.no_of_employees,
                    'company_industry': company_detail.company_industry,
                    'company_description': company_detail.company_description,
                    'company_logo_path': company_detail.company_logo_path,
                    'contact_person_name': company_detail.contact_person_name,
                    'contact_person_position': company_detail.contact_person_position,
                    'company_website_link': company_detail.company_website_link,
                    'addresses': addresses,  # List of addresses
                })

            df = pd.DataFrame(data)

            # Exporting DataFrame to Excel
            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)

            # Send email with the Excel file attached
            subject = 'Company Details Table Report'
            message = 'Please find the attached Company details table report.'
            from_email = 'brochill547@gmail.com'
            recipient_list = ['brochill547@gmail.com']
            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach('company_details_report.xlsx', excel_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()

            self.stdout.write(self.style.SUCCESS('Company details table report sent successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
