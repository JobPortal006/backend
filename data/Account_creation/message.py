from django.http import JsonResponse

#dynamic success response
def handleSuccess(success):
    return JsonResponse({"status":True,"statusCode":200,"message":success},safe=False)

#dynamic error response
def errorResponse(error):
    return  JsonResponse({"status":False,"statusCode":404,"message":error},safe=False)

#server error response
def serverErrorResponse():
    return  JsonResponse({"status":False,"statusCode":500,"message":"Internal Server Error"},safe=False)

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
            'accountCreation':'Account Created Successfully'
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
            'FileError':' Invalid file format. Allowed formats: jpg, jpeg, png, pdf'
        }
    }
    if val == 'Success':
        return handleSuccess(key_value_mapping[val][key])
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