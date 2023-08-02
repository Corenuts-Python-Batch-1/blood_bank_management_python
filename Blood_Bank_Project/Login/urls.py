from django.urls import path
from . import views

urlpatterns = [
    path('getall/registerdetails/',views.RegisterDetails.as_view(), name='getregisterdetails'),
    path('get/registerdetails/<int:pk>/',views.RegisterDetails.as_view(), name='getregisterdetails'),
    path('create/registerdetails/',views.RegisterDetails.as_view(), name='createregisterdetails'),
    path('update/registerdetails/<int:pk>/',views.RegisterDetails.as_view(), name='updateregisterdetails'),
    path('delete/registerdetails/<int:pk>/',views.RegisterDetails.as_view(), name='deleteregisterdetails'),
    path('login/',views.LoginDetails.as_view(), name='login' ),
    path('get/logindetails/', views.UserDetails.as_view(), name="logindetails" ),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    # path('forgot/',views.ForgotPasswordAPIView.as_view(),name='forgot')
]