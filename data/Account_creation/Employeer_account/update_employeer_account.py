from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Employeer_account.Query import update_employeer_account_query
from data.Account_creation.Query import create_account_user_query
from data.message import create_session

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

        # street_permanent = request.POST.get('street')
        # city_permanent = request.POST.get('city')
        # state_permanent = request.POST.get('state')     
        # country_permanent = request.POST.get('country')
        # pincode_permanent = request.POST.get('pincode')
        # address_type_permanent = request.POST.get('address_type')
        # print("address_type:", address_type_permanent)
        # print("city:", city_permanent)
        # print("country:", country_permanent)
        # print("pincode:", pincode_permanent)
        # print("state:", state_permanent)
        # print("street:", street_permanent)

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

        employee_id, registered_by , email_address= create_account_user_query.mobile_number(mobile_number)
        print(employee_id, registered_by, email_address)

        session = create_session()
        update_employeer_account_query.update_signup_details(session, employee_id, email, mobile_number)
        for i in range(2):  # Assuming there are at most two addresses, adjust as needed
            address_street = request.POST.get(f'address_{i}_street')
            address_city = request.POST.get(f'address_{i}_city')
            address_state = request.POST.get(f'address_{i}_state')
            address_country = request.POST.get(f'address_{i}_country')
            address_pincode = request.POST.get(f'address_{i}_pincode')
            address_type = request.POST.get(f'address_{i}_address_type')
            print(f"address_street: {address_street}")
            print(f"address_city: {address_city}")
            print(f"address_state: {address_state}")   
            print(f"address_country: {address_country}")
            print(f"address_pincode: {address_pincode}")
            print(f"address_type: {address_type}")
            if address_street is not None:
                update_employeer_account_query.update_or_create_address(session, employee_id, address_street, address_city, address_state, address_country,address_pincode, address_type)
        
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