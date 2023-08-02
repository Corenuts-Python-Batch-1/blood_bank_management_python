from django.urls import path
from UserView import views
urlpatterns=[
    path('getall/location/',views.getLocation,name='getalllocation'),
    path('get/location/<int:location_id>/',views.getLocation,name='getlocation'),
    path('create/location/',views.createLocation,name='createlocation'),
    path('update/location/<int:location_id>/',views.updateLocation,name='updatelocation'),
    path('delete/location/<int:location_id>/',views.deleteLocation,name='deletelocation'),

    path('getall/bloodgroup/',views.getBloodGroup,name='getallbloodgroup'),
    path('get/bloodgroup/<int:blood_group_id>/',views.getBloodGroup,name='getbloodgroup'),
    path('create/bloodgroup/',views.createBloodGroup,name='createbloodgroup'),
    path('update/bloodgroup/<int:blood_group_id>/',views.updateBloodGroup,name='updatebloodgroup'),
    path('delete/bloodgroup/<int:blood_group_id>/',views.deleteBloodGroup,name='deletebloodgroup'),
    path('get/location/bloodgroup/<int:location_id>/<int:blood_group_id>/',views.getBloodgroupWithLocation,name='getbloodgroupwithlocation'),

    path('getall/bloodbank/',views.getBloodBank,name='getallbloodbank'),
    path('get/bloodbank/<int:blood_bank_id>/',views.getBloodBank,name='getbloodbank'),
    path('create/bloodbank/',views.createBloodBank,name='createbloodbank'),
    path('update/bloodbank/<int:blood_bank_id>/',views.updateBloodBank,name='updatebloodbank'),
    path('delete/bloodbank/<int:blood_bank_id>/',views.deleteBloodBank,name='deletebloodbank'),

    path('getall/patientdetails/',views.getPatientDetails,name='getallpatientdetails'),
    path('get/patientdetails/<int:patient_id>/',views.getPatientDetails,name='getpatientdetails'),
    path('create/patientdetails/',views.createPatientDetails,name='createpatientdetails'),
    path('update/patientdetails/<int:patient_id>/',views.patientAccept,name='updatepatientdetails'),
    path('update/patientdetails/reject/<int:patient_id>/',views.patientReject,name='updatepatientdetails'),
    path('delete/patientdetails/<int:patient_id>/',views.deletePatientDetails,name='deletepatientdetails'),
    path('request/currentday/patientdetails/',views.currentDayRequestedPatientDetails,name='currentdayrequestedpatientdetails'),
    path('accept/currentday/patientdetails/',views.currentDayAcceptedPatientDetails,name='currentdayacceptedpatientdetails'),
    path('getall/request/currentday/patientdetails/',views.currentDayAllRequestsPatientDetails,name='currentdayallrequestedpatientdetails'),
    path('getall/request/location/patientdetails/<int:location_id>/',views.getRequestedPatientsByLocation,name='locationrequestedpatientdetails'),

    path('getall/totalunits/',views.getTotalUnits,name='getalltotalunits'),
    path('get/totalunits/<int:total_units_id>/',views.getTotalUnits,name='gettotalunits'),
    path('create/totalunits/',views.createTotalUnits,name='createtotalunits'),
    path('update/totalunits/<int:total_units_id>/',views.updateTotalUnits,name='updatetotalunits'),#getBloodgroupWithLocation
    path('delete/totalunits/<int:total_units_id>/',views.deleteTotalUnits,name='deletetotalunits'),
    path('get/totalunits/bloodgroup/',views.getTotalUnitsByBloodGroup,name='gettotalunitsbybloodgroup'),
    path('get/bloodgroup/location/<int:location_id>/',views.getBloodGroupWithTotalUnits,name='getbloodgroupwithlocation'),




]