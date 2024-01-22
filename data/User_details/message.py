def Signup():
    parameter_value = "Signup Successfully"
    return function(parameter_value)

def emailError():
    parameter_value = "Email already exists. Please use a different email address."
    return function(parameter_value)

def Login():
    parameter_value = "Login Successfully"
    return function(parameter_value)

def loginError():
    parameter_value = "Invalid email or password"
    return function(parameter_value)

def Error():
    parameter_value = "Request method should be POST"
    return function(parameter_value)

def emailSent():
    parameter_value = "Email sent Successfully"
    return function(parameter_value)

def emailSentError():
    parameter_value = "Email is not registered"
    return function(parameter_value)

def passwordUpdate():
    parameter_value = "Password updated successfully!"
    return function(parameter_value)

def function(value):
    return value