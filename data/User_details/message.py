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

def Signup():
    parameter_value = "Signup Successfully"
    return handleSuccess(parameter_value)

def Login():
    parameter_value = "Login Successfully"
    return parameter_value

def loginWithOTP():
    parameter_value = "Mobile Number is registered"
    return handleSuccess(parameter_value)

def emailSent():
    parameter_value = "Email sent Successfully"
    return handleSuccess(parameter_value)

def passwordUpdate():
    parameter_value = "Password updated successfully!"
    return handleSuccess(parameter_value)

def accountCreation():
    parameter_value = "Account Created Successfully"
    return handleSuccess(parameter_value)

def emailError():
    parameter_value = "Email already exists. Please use a different email address."
    return errorResponse(parameter_value)

def loginError():
    parameter_value = "Invalid email or password"
    return errorResponse(parameter_value)

def loginWithOTPError():
    parameter_value = "Mobile Number is not registered"
    return errorResponse(parameter_value) 

def Error():
    parameter_value = "Request method should be POST"
    return errorResponse(parameter_value)

def emailSentError():
    parameter_value = "Email is not registered"
    return errorResponse(parameter_value)

def passwordUpdateError():
    parameter_value = "Password is not updated"
    return errorResponse(parameter_value)
