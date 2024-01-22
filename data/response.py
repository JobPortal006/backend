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

