from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup, CompanyDetails, Address
from data.Account_creation.Query import create_account_user_query
from sqlalchemy.orm import declarative_base
import json
import base64

Base = declarative_base()

@csrf_exempt
def update_employee_details(request):
    try:
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_position = request.POST.get('contact_person_position')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        street_permanent = request.POST.get('street')
        city_permanent = request.POST.get('city')
        state_permanent = request.POST.get('state')
        country_permanent = request.POST.get('country')
        pincode_permanent = request.POST.get('pincode')
        address_type_permanent = request.POST.get('address_type')
        # company_logo = company_details.get('company_logo') 
        company_logo = request.FILES.get("company_logo")
        company_logo = company_logo.read()
        # print(company_logo,'image---------------')
        company_name = request.POST.get('company_name')
        company_industry = request.POST.get('company_industry')
        company_description = request.POST.get('company_description')
        no_of_employees = request.POST.get('no_of_employees')
        company_website_link = request.POST.get('company_website_link')

        # data = json.loads(request.body)
        # contact_person_name = data.get('contact_person_name')
        # contact_person_position = data.get('contact_person_position')
        # email = data.get('email')
        # mobile_number = data.get('mobile_number')
        # street_permanent = data.get('street')
        # city_permanent = data.get('city')
        # state_permanent = data.get('state')
        # country_permanent = data.get('country')
        # pincode_permanent = data.get('pincode')
        # address_type_permanent = data.get('address_type')
        # company_name = data.get('company_name')
        # company_industry = data.get('company_industry')
        # company_description = data.get('company_description')
        # no_of_employees = data.get('no_of_employees')
        # company_website_link = data.get('company_website_link')
        employee_id, registered_by , email_address= create_account_user_query.mobile_number(mobile_number)
        print(employee_id, registered_by, email_address)

        engine = create_engine('mysql://theuser:thepassword@13.51.207.189:3306/backend1')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Update Signup details
        signup_details = session.query(Signup).filter_by(id=employee_id).first()
        if signup_details:
            signup_details.email = email
            signup_details.mobile_number = mobile_number

        # Update or create Address details
        address_details = session.query(Address).filter_by(user_id=employee_id, address_type=address_type_permanent).first()
        if address_details:
            address_details.city = city_permanent
            address_details.country = country_permanent
            address_details.pincode = pincode_permanent
            address_details.state = state_permanent
            address_details.street = street_permanent
        else:
            new_address = Address(user_id=employee_id, address_type=address_type_permanent, city=city_permanent,
                                  country=country_permanent, pincode=pincode_permanent, state=state_permanent,
                                  street=street_permanent)
            session.add(new_address)

        # Update or create CompanyDetails
        company_details = session.query(CompanyDetails).filter_by(employee_id=employee_id).first()
        if company_details:
            company_details.company_name = company_name
            company_details.company_industry = company_industry
            company_details.company_description = company_description
            company_details.no_of_employees = no_of_employees
            company_details.company_website_link = company_website_link
            # company_details.company_logo = company_logo
            company_details.contact_person_name = contact_person_name
            company_details.contact_person_position = contact_person_position
        else:
            new_company_details = CompanyDetails(employee_id=employee_id, company_name=company_name,
                                                 company_industry=company_industry, company_description=company_description,
                                                 no_of_employees=no_of_employees, company_website_link=company_website_link,
                                                #  company_logo=company_logo,contact_person_name=contact_person_name,
                                                 contact_person_position=contact_person_position)
            session.add(new_company_details)

        session.commit()
        session.close()

        return JsonResponse({"success": "Data updated successfully"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed to update data"})
