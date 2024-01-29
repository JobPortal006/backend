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

def success(key):
    key_value_mapping = {
        'Signup': 'Signup Successfully',
        'Login': 'Login Successfully',
        'loginWithOTP': 'Mobile Number is registered',
        'emailSent': 'Email sent Successfully',
        'passwordUpdate':'Password updated successfully!',
        'accountCreation':'Account Created Successfully'
    }
    if key in key_value_mapping:
        return handleSuccess(key_value_mapping[key])
    else:
        return None

def error(key):
    key_value_mapping = {
        'emailError': 'Email already exists. Please use a different email address.',
        'loginError': 'Invalid email or password',
        'loginWithOTPError': 'Mobile Number is not registered',
        'emailSentError': 'Email is not registered',
        'passwordUpdateError':'Password is not updated',
        'Error':'Request method should be POST'
    }
    if key in key_value_mapping:
        return errorResponse(key_value_mapping[key])
    else:
        return None