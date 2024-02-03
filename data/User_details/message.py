from django.http import JsonResponse

#dynamic success response
def handleSuccess(success,data):
    return JsonResponse({"status":True,"statusCode":200,"message":success,"data":data},safe=False)

#dynamic error response
def errorResponse(error):
    return  JsonResponse({"status":False,"statusCode":404,"message":error},safe=False)

#server error response
def serverErrorResponse():
    return  JsonResponse({"status":False,"statusCode":500,"message":"Internal Server Error"},safe=False)

def Login():
    parameter_value = "Login Successfully"
    return parameter_value

def success(key,insert):
    key_value_mapping = {
        'Signup': 'Signup Successfully',
        'Login': 'Login Successfully',
        'loginWithOTP': 'Mobile Number is registered',
        'emailSent': 'Email sent Successfully',
        'passwordUpdate':'Password updated successfully!',
        'accountCreation':'Account Created Successfully'
    }
    
    if key in key_value_mapping:
        data = insert
        return handleSuccess(key_value_mapping[key],data)
    else:
        return None

def error(key):
    key_value_mapping = {
        'emailError': 'Email is already exists. Please use a different email address.',
        'mobileError': 'Mobilenumber is already exists. Please use a different email address.',
        'loginError': 'Invalid email or password',
        'loginWithOTPError': 'Mobile Number is not registered',
        'emailSentError': 'Email is not registered',
        'passwordUpdateError':'Password is not updated',
        'Error':'Request method should be POST',
        'InputError':'Input Should not be empty',
        'FileError':' Invalid file format. Allowed formats: jpg, jpeg, png, pdf',
        'UserIdError':'User Id is already exists'
    }
    if key in key_value_mapping:

        return errorResponse(key_value_mapping[key])
    else:
        return None
    

def data_check(email,mobile_number,password,signup_by):
    if email != '' and email != None and mobile_number != '' and mobile_number != None and password != '' and password != None and signup_by != '' and signup_by != None:
       return True
    else:
        return False
    
def personal_details(first_name, last_name, date_of_birth, gender):
    if first_name != '' and first_name != None and last_name != '' and last_name != None and date_of_birth != '' and date_of_birth != None and gender != '' and gender != None:
       return True
    else:
        return False
    
    
def address_details_permanent(street_permanent, city_permanent, state_permanent, country_permanent,
                            pincode_permanent, address_type_permanent):
    if (street_permanent != '' and street_permanent != None and 
    city_permanent != '' and city_permanent != None and state_permanent != '' and state_permanent != None and country_permanent != '' and country_permanent != None and 
    pincode_permanent != '' and pincode_permanent != None and address_type_permanent != '' and address_type_permanent != None) :
        return True
    else:
        return False
    
def educational_details(sslc_school_name, sslc_start_year, sslc_end_year, sslc_percentage, hsc_school_name,
                        hsc_start_year, hsc_end_year, hsc_percentage, college_name, college_start_year, college_end_year,
                        college_percentage, department, degree):
    if (sslc_school_name != '' and sslc_school_name != None and sslc_start_year != '' and sslc_start_year != None and 
    sslc_end_year != '' and sslc_end_year != None and sslc_percentage != '' and sslc_percentage != None and hsc_school_name != '' and hsc_school_name != None and 
    hsc_start_year != '' and hsc_start_year != None and hsc_end_year != '' and hsc_end_year != None and hsc_percentage != '' and hsc_percentage != None and 
    college_name != '' and college_name != None and college_start_year != '' and college_start_year != None and college_end_year != '' and college_end_year != None and 
    college_percentage != '' and college_percentage != None and department != '' and department != None and degree != '' and degree != None) :
        return True
    else:
        return False
    
def job_preference_details(key_skills, department, industry, prefered_locations):
    if (key_skills != '' and key_skills != None and department != '' and department != None and 
    industry != '' and industry != None and prefered_locations != '' and prefered_locations != None) :
        return True
    else:
        return False
    
def rowcount(rows_affected):
  if rows_affected > 0:
    data = f'Data is affected in {rows_affected} row in the table'
    return data