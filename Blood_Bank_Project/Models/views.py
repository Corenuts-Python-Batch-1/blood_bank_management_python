from django.shortcuts import render
from Login.views import UserDetails,AdminDetails
# Create your views here.
def UserValidated(request):
    user_details = UserDetails()
    return user_details.get(request)

def AdminValidated(request):
    admin_details = AdminDetails()
    return  admin_details.get(request)
    