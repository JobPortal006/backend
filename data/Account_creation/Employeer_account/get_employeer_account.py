from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup,CompanyDetails,Address
from sqlalchemy.orm import declarative_base
import json
import base64

Base = declarative_base()

@csrf_exempt
def get_employeer_details(request):
    try:
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        print(employee_id)
        engine = create_engine('mysql://theuser:thepassword@13.51.207.189:3306/backend1')

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine) 
        session = Session()

        employeer_details = {}
        signup_details = session.query(Signup).filter_by(id=employee_id).first()
        if signup_details:
          employeer_details['Signup'] = {
            'email': signup_details.email,
            'mobile_number': signup_details.mobile_number
          }
        # print(employeer_details,'2-------------')
        address_details = session.query(Address).filter_by(user_id=employee_id).all()
        # employeer_details['address'] = {}
        for address in address_details:
            employeer_details['company_address'] = {
                'address_type': address.address_type,
                'city': address.city,
                'country': address.country,
                'pincode': address.pincode,
                'state': address.state,
                'street': address.street,
            }
        # print(employeer_details,'3-------------')

        company_details = session.query(CompanyDetails).filter_by(employee_id=employee_id).first()
        if company_details:
            company_logo = company_details.company_logo
            company_logo_base64 = base64.b64encode(company_logo).decode('utf-8') if company_logo else None
            employeer_details['company_details'] = {
                'company_name': company_details.company_name,
                'company_industry': company_details.company_industry,
                'company_description': company_details.company_description,
                'no_of_employees': company_details.no_of_employees,
                'company_website_link': company_details.company_website_link,
                'contact_person_name': company_details.contact_person_name,
                'contact_person_position': company_details.contact_person_position,
                'company_logo': company_logo_base64
            }
        session.close()
        return JsonResponse(employeer_details)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed"})


