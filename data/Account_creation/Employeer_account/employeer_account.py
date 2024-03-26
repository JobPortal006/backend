import boto3
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from data.Account_creation.Query import create_account_employeer_query, create_account_user_query
from data import message
import io
import json
from data.token import decode_token

@method_decorator(csrf_exempt, name='dispatch') # Dispatch method is handle HTTP method (GET, POST, etc.) 
class employer_register(View): # View class provides a creating views by defining methods for different HTTP methods (e.g., get, post).
    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                contact_person_name = request.POST.get('contact_person_name')
                contact_person_position = request.POST.get('contact_person_position')
                email = request.POST.get('email')
                mobile_number = request.POST.get('mobile_number')
                token = request.POST.get('token')
                print(token)
                company_logo = request.FILES.get("company_logo")
                company_logo_name = company_logo.name
                company_logo_content = company_logo.read()
                company_name = request.POST.get('company_name')
                company_industry = request.POST.get('company_industry')
                company_description = request.POST.get('company_description')
                no_of_employees = request.POST.get('no_of_employees')
                company_website_link = request.POST.get('company_website_link')
                employee_id,registered_by,email = decode_token(token)
                print(employee_id, registered_by,email)
                if employee_id is not None:
                    if email:
                        s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
                        company_logo_path = f'company_logo/{employee_id}_{company_logo_name}'
                        s3.upload_fileobj(io.BytesIO(company_logo_content), 'backendcompanylogo', company_logo_path)
                        print(company_logo_path)
                        # Check permanent address details data is empty or not
                        userid_check = create_account_employeer_query.userid_check(employee_id)
                        print(userid_check)
                        if userid_check: 
                            company_details_data = message.company_details(company_logo,company_name,company_industry, company_description, no_of_employees,company_website_link)
                            print(company_details_data)
                            if company_details_data:
                                company_details_result = create_account_employeer_query.company_details(employee_id,company_name,
                                    company_industry,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position,company_logo_path)
                                print('Company_details_result ->', company_details_result)
                                if company_details_result:
                                    company_address_json = request.POST.get('company_address', '[]')
                                    company_addresses = json.loads(company_address_json)
                                    # Get the length of the array of objects
                                    num_addresses = len(company_addresses)
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
                                            address_details_permanent_result = create_account_user_query.address_details(
                                                employee_id, registered_by, address_street, address_city, address_state, address_country,
                                                address_pincode, address_type)
                                            print('Address_details_permanent ->',i, address_details_permanent_result)
                                # sending email
                                subject = 'Account Creation'
                                message_html = render_to_string('account.html', {'name': contact_person_name})
                                message_plain = strip_tags(message_html)
                                from_email = 'brochill547@gmail.com'
                                recipient_list = [email]
                                send_mail(subject, message_plain, from_email, recipient_list, html_message=message_html)
                            if company_details_result:
                                return message.response('Success','accountCreation')
                            else:
                                return message.response('Error','employeeAccountError')
                        else:
                            return message.response('Error','UserIdError')
                    else:
                        return message.response('Error','emailSentError')
                else:
                    return message.response('Error', 'tokenError')
            else:
                return message.response('Error','Error')
        except Exception as e:
            print(str(e))
            return message.serverErrorResponse()
    