from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup, CompanyDetails, Address
from sqlalchemy.orm import declarative_base
import json
import base64
import boto3 

Base = declarative_base()

@csrf_exempt
def get_employeer_details(request):
    try:
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        print(employee_id)
        engine = create_engine('mysql://theuser:thepassword@16.171.137.133:3306/backend1')

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        employeer_details = {}
        
        # Retrieve Signup details
        signup_details = session.query(Signup).filter_by(id=employee_id).first()
        if signup_details:
            employeer_details['Signup'] = {
                'email': signup_details.email,
                'mobile_number': signup_details.mobile_number
            }

        # Retrieve Address details
        address_details = session.query(Address).filter_by(user_id=employee_id).all()
        for address in address_details:
            employeer_details['company_address'] = {
                'address_type': address.address_type,
                'city': address.city,
                'country': address.country,
                'pincode': address.pincode,
                'state': address.state,
                'street': address.street,
            }

        # Retrieve CompanyDetails
        company_details = session.query(CompanyDetails).filter_by(employee_id=employee_id).first()
        if company_details:
            # Retrieve company logo from S3
            # company_logo = company_details.company_logo
            # company_logo_base64 = base64.b64encode(company_logo).decode('utf-8') if company_logo else None
            company_logo_base64 = get_company_logo_from_s3(company_details.company_logo_path)
            
            employeer_details['company_details'] = {
                'company_name': company_details.company_name,
                'company_industry': company_details.company_industry,
                'company_description': company_details.company_description,
                'no_of_employees': company_details.no_of_employees,
                'company_website_link': company_details.company_website_link,
                'contact_person_name': company_details.contact_person_name,
                'contact_person_position': company_details.contact_person_position,
                'company_logo': company_logo_base64,
                'company_logo_path':company_details.company_logo_path
            }

        session.close()
        return JsonResponse(employeer_details)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed"})

def get_company_logo_from_s3(s3_key):
    # Retrieve company logo from S3 and return as Base64
    s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
    try:
        print(s3_key)
        response = s3.get_object(Bucket='backendcompanylogo', Key=s3_key)
        company_logo_content = response['Body'].read()
        company_logo_base64 = base64.b64encode(company_logo_content).decode('utf-8')
        return company_logo_base64
    except Exception as e:
        print(f"Error retrieving company logo from S3: {str(e)}")
        return None
