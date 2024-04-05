from django.http import JsonResponse
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

#dynamic success response
def handleSuccess(success):
    return JsonResponse({"status": True, "statusCode": 200, "message": success})

def handleSuccess1(success,data):
    return JsonResponse({"status":True,"statusCode":200,"message":success,"data":data})

#dynamic error response
def errorResponse(error):
    return  JsonResponse({"status":False,"statusCode":404,"message":error})

#server error response
def serverErrorResponse():
    # manage_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'manage.py')
    # os.utime(manage_py_path, None)
    return  JsonResponse({"status":False,"statusCode":500,"message":"Internal Server Error"})

def tryExceptError(message):
    # serverReload()
    return  JsonResponse({f"status":False,"statusCode":500,"message":message})

def serverReload():
    manage_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'manage.py')
    os.utime(manage_py_path, None)

def Login():
    return "Login Successfully"
 
def response(val,key):
    key_value_mapping = {
        'Success':{
            'Signup': 'Signup Successfully',
            'Login': 'Login Successfully',
            'loginWithOTP': 'Mobile Number is registered',
            'emailSent': 'Email sent Successfully',
            'passwordUpdate':'Password updated successfully!',
            'accountCreation':'Account Created Successfully',
            'postJob':'Successfully post a job',
            'searchJob':'Job find successfully',
            'getSearchJob':'Get job result successfully',
            'updatePostJob':'Successfully Update',
            'deletePostJob':'Job deleted successfully',
            'updateData':'Data Updated Successfully',
            'applyJob':'Job Applied Successfully',
            'token':'Token is not expired',
            'getJobDetails':'Job find successfully',
            'userApplyJob':False,
            'userApplyJobResult':True,
            'savedJob':"Job Saved Successfully",
            'savedUnJob':"Job UnSaved Successfully"
        },
        'Error':{
            'emailError': 'Email is already exists. Please use a different email address.',
            'mobileError': 'Mobilenumber is already exists. Please use a different mobile number.',
            'loginError': 'Invalid email or password',
            'loginWithOTPError': 'Mobile Number is not registered',
            'emailSentError': 'Email is not registered',
            'passwordUpdateError':'Password is not updated',
            'employeeAccountError':'Account is not created',
            'Error':'Request method should be POST',
            'InputError':'Input Should not be empty',
            'FileError':' Invalid file format. Allowed formats: jpg, jpeg, png, pdf',
            'UserIdError':'You have already registered',
            'postJobError' :'Failed to Post a job',
            'companyError':'You have not completed the registration process',
            'searchJobError':'No data found',
            'UpdateJobPost_Method':'Use to PUT method',
            'getMethod':'Use to GET method',
            'deleteJobPost_Method':'Use to DELETE method',
            'updateJobError':'Job not updated successguly',
            'userApplyJobError':'You already applied for this job',
            'applyJobError':'Job apply failed',
            'tokenError':'Token is expired',
            'ValuesCheckError':'Input Should not be empty',
            'EmptyRequestBody':'Empty Request Body',
            'userJobViewError':'User not applied for this job',
            'savedJobError':"Job not Saved",
            'alreadySavedJobError':'Record already exists',
            'invalidJSON':'Invalid JSON format in request body'
        }
    }
    if val == 'Success':
        return handleSuccess(key_value_mapping[val][key])
    else:
        return errorResponse(key_value_mapping[val][key])
    
Base = declarative_base()   
def create_session():
    engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/jobportal')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
    
def response1(val,key,data):
    key_value_mapping = {
        'Success':{
            'postJob':'Successfully post a job',
            'searchJob':'Job find successfully',
            'getSearchJob':'Get job result successfully',
            'getJobDetails':'Job find successfully',
            'userApplyJob':False,
            'userApplyJobResult':True
        },  
        'Error':{
            'companyError':'You have not completed the registration process',
            'searchJobError':'No data found',
            'ValuesCheckError':'Input Should not be empty',
            'EmptyRequestBody':'Empty Request Body',
            'userApplyJobError':'You already applied for this job',
            'userJobViewError':'User not applied for this job'
        }
    }
    if val == 'Success':
        return handleSuccess1(key_value_mapping[val][key],data)
    else:
        return errorResponse(key_value_mapping[val][key])

    
def check(*args):
    for i in args:
        if i == '' or i is None:
            return False
    return True

def data_check(email, mobile_number, password, signup_by):
    values = email, mobile_number, password, signup_by
    result = check(*values)
    return result

def personal_details(first_name, last_name, date_of_birth, gender):
    values = first_name, last_name, date_of_birth, gender
    result = check(*values)
    return result
    
def address_details_permanent(street_permanent,city_permanent,state_permanent,country_permanent,pincode_permanent,address_type_permanent):
    values = street_permanent, city_permanent, state_permanent, country_permanent,pincode_permanent, address_type_permanent
    result = check(*values)
    return result
    
def educational_details(sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,hsc_start_year, hsc_end_year, 
                        hsc_percentage, college_name, college_start_year, college_end_year,college_percentage, department, degree):
    values = sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,hsc_start_year, hsc_end_year, hsc_percentage, college_name, college_start_year, college_end_year,college_percentage, department, degree
    result = check(*values)
    return result
    
def job_preference_details(key_skills, department, industry, prefered_locations):
    values = key_skills, department, industry, prefered_locations
    result = check(*values)
    return result

def company_details(company_logo,company_name,industry_type, company_description, no_of_employees,company_website_link):
    values = company_logo,company_name,industry_type, company_description, no_of_employees,company_website_link
    result = check(*values)
    return result

def searchcheck(location,experience):
    values = location,experience
    result = check(*values)
    return result