from django.urls import path
from . import views

urlpatterns = [
    path('getall/donordetails/',views.getDonorDetails, name='getlldonordetails'),
    path('update/donordetails/<int:donar_id>/',views.updateDonorDetails, name='updatedonordetails'),
    path('get/donordetails/<int:donar_id>/',views.getDonorDetails, name='getdonordetails'),
    path('delete/donordetails/<int:donar_id>/',views.deleteDonorDetails, name='deletedonordetails'),
    path('create/donordetails/',views.createDonorDetails, name='createdonordetails'),
    path('currentday/donordetails/',views.currentDayDonorDetails, name='currentdaydonordetails')

]