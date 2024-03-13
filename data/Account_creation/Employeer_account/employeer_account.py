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

@method_decorator(csrf_exempt, name='dispatch') # Dispatch method is handle HTTP method (GET, POST, etc.) 
class employer_register(View): # View class provides a creating views by defining methods for different HTTP methods (e.g., get, post).
    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                # data = json.loads(request.body)
                # if data is not None or data != '':
                #     contact_information = data.get('contact_information', {})
                #     address_data = data.get('company_address', {})
                #     company_details = data.get('company_details', {})
                #     contact_person_name = contact_information.get('contact_person_name')
                #     contact_person_position = contact_information.get('contact_person_position')
                #     email = contact_information.get('email')
                #     mobile_number = contact_information.get('mobile_number')

                #     address_type_permanent = address_data.get('address_type')
                #     city_permanent = address_data.get('city')
                #     country_permanent = address_data.get('country')
                #     pincode_permanent = address_data.get('pincode')
                #     state_permanent = address_data.get('state')
                #     street_permanent = address_data.get('street')

                #     company_logo = company_details.get('company_logo')
                #     company_name = company_details.get('company_name')
                #     company_industry = company_details.get('company_industry')
                #     company_description = company_details.get('company_description')
                #     no_of_employees = company_details.get('no_of_employees')
                #     company_website_link = company_details.get('company_website_link')
                # else:
                # contact_information = json.loads(request.POST.get('contact_information', '{}'))
                # address_data = json.loads(request.POST.get('company_address', '{}'))
                # company_details = json.loads(request.POST.get('company_details', '{}'))

                contact_person_name = request.POST.get('contact_person_name')
                contact_person_position = request.POST.get('contact_person_position')
                email = request.POST.get('email')
                mobile_number = request.POST.get('mobile_number')
                print(mobile_number)

                # street_permanent = request.POST.get('street')
                # city_permanent = request.POST.get('city')
                # state_permanent = request.POST.get('state')
                # country_permanent = request.POST.get('country')
                # pincode_permanent = request.POST.get('pincode')
                # address_type_permanent = request.POST.get('address_type')

                company_logo = request.FILES.get("company_logo")
                company_logo_name = company_logo.name
                company_logo_content = company_logo.read()  # Read the content of the file

                # print(company_logo,'image---------------')
                company_name = request.POST.get('company_name')
                company_industry = request.POST.get('company_industry')
                company_description = request.POST.get('company_description')
                no_of_employees = request.POST.get('no_of_employees')
                company_website_link = request.POST.get('company_website_link')
                user_id, registered_by , email_address= create_account_user_query.mobile_number(mobile_number)
                print(user_id, registered_by, email_address)
                if user_id:
                    if email_address == email:
                        s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
                        company_logo_path = f'company_logo/{user_id}_{company_logo_name}'
                        s3.upload_fileobj(io.BytesIO(company_logo_content), 'backendcompanylogo', company_logo_path)
                        print(company_logo_path)

                        # Check permanent address details data is empty or not
                        userid_check = create_account_employeer_query.userid_check(user_id)
                        print(userid_check)
                        if userid_check:    
                            # address_details_permanent_data= message.address_details_permanent(
                            #         street_permanent, city_permanent, state_permanent, country_permanent,
                            #         pincode_permanent, address_type_permanent)
                            # Check company details data is empty or not
                            company_details_data = message.company_details(company_logo,company_name,company_industry, company_description, no_of_employees,company_website_link)
                            print(company_details_data)
                            if company_details_data:
                                address_id = create_account_employeer_query.get_id(user_id,registered_by)
                                # address_id = 1
                                company_details_result = create_account_employeer_query.company_details(user_id,company_logo_content,company_name,
                                    company_industry,company_description, no_of_employees,company_website_link,contact_person_name,contact_person_position,address_id,company_logo_path)
                                print('Company_details_result ->', company_details_result)
                                if company_details_result:
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
                                            address_details_data = message.address_details_permanent(
                                                address_street,
                                                address_city,
                                                address_state,
                                                address_country,
                                                address_pincode,
                                                address_type)
                                        address_details_permanent_result = create_account_user_query.address_details(
                                            user_id, registered_by, address_street, address_city, address_state, address_country,
                                            address_pincode, address_type)
                                        print('Address_details_permanent ->', address_details_permanent_result)

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
                    return message.response('Error','loginWithOTPError')
            else:
                return message.response('Error','Error')
        except Exception as e:
            print(str(e))
            return message.serverErrorResponse()
    