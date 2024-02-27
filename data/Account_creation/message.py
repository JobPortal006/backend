from django.http import JsonResponse

#dynamic success response
def handleSuccess(success):
    return JsonResponse({"status": True, "statusCode": 200, "message": success})

def handleSuccess1(success,data):
    return JsonResponse({"status":True,"statusCode":200,"message":success,"data":data},safe=False)

#dynamic error response
def errorResponse(error):
    return  JsonResponse({"status":False,"statusCode":404,"message":error},safe=False)

#server error response
def serverErrorResponse():
    return  JsonResponse({"status":False,"statusCode":500,"message":"Internal Server Error"},safe=False)

def tryExceptError(message):
    return  JsonResponse({f"status":False,"statusCode":500,"message":message},safe=False)

def Login():
    parameter_value = "Login Successfully"
    return parameter_value

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
            'updatePostJob':'Successfully Update',
            'deletePostJob':'Job deleted successfully'
        },
        'Error':{
            'emailError': 'Email is already exists. Please use a different email address.',
            'mobileError': 'Mobilenumber is already exists. Please use a different email address.',
            'loginError': 'Invalid email or password',
            'loginWithOTPError': 'Mobile Number is not registered',
            'emailSentError': 'Email is not registered',
            'passwordUpdateError':'Password is not updated',
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
        }
    }
    if val == 'Success':
        return handleSuccess(key_value_mapping[val][key])
    else:
        return errorResponse(key_value_mapping[val][key])
    
def response1(val,key,data):
    key_value_mapping = {
        'Success':{
            'postJob':'Successfully post a job',
            'searchJob':'Job find successfully',
            'getSearchJob':'Get job result successfully',
            'getJobDetails':'Job result get successgully'
        },  
        'Error':{
            'companyError':'You have not completed the registration process',
            'searchJobError':'No data found',
            'ValuesCheckError':'Input Should not be empty',
            'EmptyRequestBody':'Empty Request Body '
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