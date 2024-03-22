from data.Account_creation.Tables.table import Signup, CompanyDetails, Address
import io
import boto3

# Update Signup details
def update_signup_details(session, employee_id, email, mobile_number):
    signup_details = session.query(Signup).filter_by(id=employee_id).first()
    if signup_details:
        signup_details.email = email
        signup_details.mobile_number = mobile_number

# Update or create Address details
def update_or_create_address(session, employee_id,registered_by, street, city, state, country,pincode, address_type):
    new_address = Address(user_id=employee_id,registered_by=registered_by, address_type=address_type, city=city,
                            country=country, pincode=pincode, state=state, street=street)
    session.add(new_address)

# Update or create CompanyDetails
def update_or_create_company_details(session, employee_id, company_name, company_industry, company_description,
                                     no_of_employees, company_website_link, contact_person_name, contact_person_position,
                                     company_logo_key):
    company_details = session.query(CompanyDetails).filter_by(employee_id=employee_id).first()
    if company_details:
        company_details.company_name = company_name
        company_details.company_industry = company_industry
        company_details.company_description = company_description
        company_details.no_of_employees = no_of_employees
        company_details.company_website_link = company_website_link
        company_details.contact_person_name = contact_person_name
        company_details.contact_person_position = contact_person_position
        company_details.company_logo_path = company_logo_key
    else:
        new_company_details = CompanyDetails(employee_id=employee_id, company_name=company_name,
                                             company_industry=company_industry, company_description=company_description,
                                             no_of_employees=no_of_employees, company_website_link=company_website_link,
                                             contact_person_name=contact_person_name,
                                             contact_person_position=contact_person_position,
                                             company_logo_path=company_logo_key)
        session.add(new_company_details)

def get_company_logo_path(session,employee_id):
    company_details = session.query(CompanyDetails).filter_by(employee_id=employee_id).first()
    company_logo_key=company_details.company_logo_path 
    if company_logo_key:
        return company_logo_key
    else:
        return None

def update_company_logo_file(company_logo, company_logo_name, employee_id, existing_logo_key):
    print('file--------')
    print(company_logo_name)
    # existing_logo_key='39_testing.png'
    s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
    # if existing_logo_key is not None:
    # try:
    #     print('existing_logo_key------')
    #     s3.delete_object(Bucket='backendcompanylogo', Key="testing.png")
    #     print(f"Existing object with key ' deleted from S3.")
    # except Exception as e:
    #     print(f"Error deleting existing object: {e}")
    new_logo_key = f'company_logo/{employee_id}_{company_logo_name}'
    # company_logo_contents = company_logo.read()
    if existing_logo_key != new_logo_key:
        s3.upload_fileobj(io.BytesIO(company_logo), 'backendcompanylogo', new_logo_key)
    return new_logo_key
    
# def update_company_logo_file( company_logo_name, employee_id, existing_logo_key):
#     print(' working fine------->2')
#     s3 = boto3.client('s3',aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
#     print(' working fine------->3')

#     new_logo_path = f'{employee_id}_{company_logo_name}'
#     # new_logo_path= '39_Screenshot+(1).png'
#     print(new_logo_path+""+' working fine------->4')
#     try:
#         if not os.path.isfile(new_logo_path):
#             print('try block workig ------>5')
#         print(' working fine------->6')
#         with open(new_logo_path,'rb') as new_image_file:
#             print(' working fine------->7')
#             s3.upload_fileobj(new_image_file,'backendcompanylogo' , existing_logo_key )
#     except FileNotFoundError:
#         print(f'error the file {new_logo_path} not found')
#     except Exception as e:
#         print(f'an error occureed: {str(e)}')


# def update_company_logo_file(company_logo, company_logo_name, employee_id, existing_logo_key):
#     print('file--------')
#     print(company_logo_name)
#     s3 = boto3.client('s3', aws_access_key_id='AKIAZI2LB2XIRFQPYDJ4', aws_secret_access_key='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', region_name='eu-north-1')
#     if existing_logo_key is not None:
#         try:
#             s3.delete_object(Bucket='backendcompanylogo', Key=existing_logo_key)
#             print(f"Existing object with key '{existing_logo_key}' deleted from S3.")
#         except Exception as e:
#             print(f"Error deleting existing object: {e}")
#     if company_logo_name is None:
#         company_logo_contents = company_logo.read()
#         new_logo_key = company_logo.name
#     else:
#         new_logo_key = f'company_logo/{employee_id}_{company_logo_name}'
#         company_logo_contents = company_logo.read()
#     print(new_logo_key, 'newlogokey----------')
#     if existing_logo_key != new_logo_key:
#         print(existing_logo_key, 'existing_logo_key-----------')
#         s3.upload_fileobj(io.BytesIO(company_logo_contents), 'backendcompanylogo', new_logo_key)
#     return new_logo_key