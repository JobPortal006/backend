from django.http import JsonResponse


#dynamic success response
def handleSuccess(message):
    print("printing success function starts here")
    return JsonResponse({"status":True,"statusCode":200,"message":message},safe=False)

#dynamic error response
def errorResponse(message):
    return  JsonResponse({"status":False,"statusCode":404,"message":message},safe=False)

#server error response
def serverErrorResponse():
    return  JsonResponse({"status":False,"statusCode":500,"message":"Internal Server Error"},safe=False)