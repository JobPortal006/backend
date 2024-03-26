from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Employeer_account.Query import update_employeer_account_query
from data import message
from data.Account_creation.Tables.table import Address
from data.token import decode_token
@csrf_exempt
def update_employee_details(request):
    try:
        token = request.POST.get('token')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_position = request.POST.get('contact_person_position')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
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
        employee_id,registered_by,email = decode_token(token)
        print(employee_id, registered_by,email)
        if employee_id is not None:
            session = message.create_session()
            update_employeer_account_query.update_signup_details(session, employee_id, email, mobile_number)
            # Delete existing address data for the given user_id and address_type
            company_address_json = request.POST.get('company_address', '[]')
            # Parse the JSON string to get the array of objects
            company_addresses = json.loads(company_address_json)
            # Get the length of the array of objects
            num_addresses = len(company_addresses)
            # print("Number of addresses:", num_addresses)
            session.query(Address).filter_by(user_id=employee_id).delete()
            for i in range(num_addresses):  # Assuming there are at most two addresses, adjust as needed
                current_address = company_addresses[i]
                # Extract individual fields from the address object
                address_street = current_address.get('street')
                address_city = current_address.get('city')
                address_state = current_address.get('state')
                address_country = current_address.get('country')
                address_pincode = current_address.get('pincode')
                address_type = current_address.get('address_type')
                if address_street is not None: 
                    update_employeer_account_query.update_or_create_address(session, employee_id,registered_by, address_street, address_city, address_state, address_country,address_pincode, address_type)
            existing_logo_key = update_employeer_account_query.get_company_logo_path(session,employee_id)
            if company_logo_file is not None:
                company_logo_key = update_employeer_account_query.update_company_logo_file(company_logo_path, company_logo_name, employee_id, existing_logo_key)

            else:       
                company_logo_key = company_logo_path
            update_employeer_account_query.update_or_create_company_details(session, employee_id, company_name, company_industry, company_description,
                                            no_of_employees, company_website_link, contact_person_name,
                                            contact_person_position,company_logo_key)
            session.commit()
            session.close()
            return message.response('Success', 'updateData')
        else:
            return message.response('Error', 'tokenError')
    except Exception as e:
        print(str(e))
        return message.tryExceptError(str(e))
    
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