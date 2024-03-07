from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from data.Account_creation.Employeer_account.Query.update_employeer_account_query import update_signup_details,get_company_logo_path,update_or_create_address,update_or_create_company_details,update_company_logo_file,upload_company_logo_path
# from data.Account_creation.Tables.table import Signup, CompanyDetails, Address
from data.Account_creation.Employeer_account.Query import update_employeer_account_query
from data.Account_creation.Query import create_account_user_query
from sqlalchemy.orm import declarative_base
# import io
# import boto3
from backend.data.message import create_session

# Base = declarative_base()

@csrf_exempt
def update_employee_details(request):
    try:
        contact_person_name = request.POST.get('contact_person_name')
        print("contact_person_name:", contact_person_name)

        contact_person_position = request.POST.get('contact_person_position')
        print("contact_person_position:", contact_person_position)
        email = request.POST.get('email')
        print("email:", email)

        mobile_number = request.POST.get('mobile_number')
        print("mobile_number:", mobile_number)

        street_permanent = request.POST.get('street')
        city_permanent = request.POST.get('city')
        state_permanent = request.POST.get('state')     
        country_permanent = request.POST.get('country')
        pincode_permanent = request.POST.get('pincode')
        address_type_permanent = request.POST.get('address_type')
        print("address_type:", address_type_permanent)
        print("city:", city_permanent)
        print("country:", country_permanent)
        print("pincode:", pincode_permanent)
        print("state:", state_permanent)
        print("street:", street_permanent)

        # Correct way to handle file upload for company logo
        company_logo_file = request.FILES.get("company_logo_path")
        if company_logo_file is None:
            company_logo_path = request.POST.get('company_logo_path')
        else:
            company_logo_name=company_logo_file.name
            company_logo_path = company_logo_file.read()
            print(company_logo_name)

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

        # engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/backend1')
        # Base.metadata.create_all(engine)
        # Session = sessionmaker(bind=engine)
        # session = Session()
        session = create_session()
        update_employeer_account_query.update_signup_details(session, employee_id, email, mobile_number)
        update_employeer_account_query.update_or_create_address(session, employee_id, address_type_permanent, city_permanent, country_permanent,
                                 pincode_permanent, state_permanent, street_permanent)
        
        existing_logo_key = update_employeer_account_query.get_company_logo_path(session,employee_id)
        print(existing_logo_key,'e------')
        if company_logo_file is not None:
            company_logo_key = update_employeer_account_query.update_company_logo_file(company_logo_path, company_logo_name, employee_id, existing_logo_key)

        else:       
            company_logo_key = company_logo_path
        update_employeer_account_query.update_or_create_company_details(session, employee_id, company_name, company_industry, company_description,
                                         no_of_employees, company_website_link, contact_person_name,
                                         contact_person_position,company_logo_key)
        session.commit()
        session.close()

        return JsonResponse({"success": "Data updated successfully"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed to update data"})

# # Update Signup details
# def update_signup_details(session, employee_id, email, mobile_number):
#     signup_details = session.query(Signup).filter_by(id=employee_id).first()
#     if signup_details:
#         signup_details.email = email
#         signup_details.mobile_number = mobile_number

# # Update or create Address details
# def update_or_create_address(session, employee_id, address_type, city, country, pincode, state, street):
#     address_details = session.query(Address).filter_by(user_id=employee_id, address_type=address_type).first()
#     if address_details:
#         address_details.city = city
#         address_details.country = country
#         address_details.pincode = pincode
#         address_details.state = state
#         address_details.street = street
#     else:
#         new_address = Address(user_id=employee_id, address_type=address_type, city=city,
#                               country=country, pincode=pincode, state=state, street=street)
#         session.add(new_address)

# # Update or create CompanyDetails
# def update_or_create_company_details(session, employee_id, company_name, company_industry, company_description,
#                                      no_of_employees, company_website_link, contact_person_name, contact_person_position,
#                                      company_logo_key):
#     company_details = session.query(CompanyDetails).filter_by(employee_id=employee_id).first()
#     if company_details:
#         company_details.company_name = company_name
#         company_details.company_industry = company_industry
#         company_details.company_description = company_description
#         company_details.no_of_employees = no_of_employees
#         company_details.company_website_link = company_website_link
#         company_details.contact_person_name = contact_person_name
#         company_details.contact_person_position = contact_person_position
#         company_details.company_logo_path = company_logo_key
#     else:
#         new_company_details = CompanyDetails(employee_id=employee_id, company_name=company_name,
#                                              company_industry=company_industry, company_description=company_description,
#                                              no_of_employees=no_of_employees, company_website_link=company_website_link,
#                                              contact_person_name=contact_person_name,
#                                              contact_person_position=contact_person_position,
#                                              company_logo_path=company_logo_key)
#         session.add(new_company_details)

# def get_company_logo_path(session,employee_id):
#     company_details = session.query(CompanyDetails).filter_by(employee_id=employee_id).first()
#     company_logo_key=company_details.company_logo_path 
#     if company_logo_key:
#         return company_logo_key
#     else:
#         return None

# def upload_logo_to_s3(company_logo, company_logo_name, employee_id,existing_logo_key):
#     s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
#     new_logo_key = f'company_logo/{employee_id}_{company_logo_name}'

#     # Check if the new logo key is different from the existing one
#     if existing_logo_key != new_logo_key:
#         s3.upload_fileobj(io.BytesIO(company_logo), 'backendcompanylogo', new_logo_key)
#         if existing_logo_key:
#             s3.delete_object(Bucket='backendcompanylogo', Key=existing_logo_key)
#             print(f"Existing object with key '{existing_logo_key}' deleted from S3.")
#     return new_logo_key
    
import boto3
@csrf_exempt
def delete_image(request):
    session=boto3.Session(
        aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', 
        aws_secret_access_key='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'
    )
    print(session)
    s3 = session.resource('s3')
    result=s3.meta.client.delete_object(Bucket='backendcompanylogo', Key="company_logo/39_39_testing")
    print(result)