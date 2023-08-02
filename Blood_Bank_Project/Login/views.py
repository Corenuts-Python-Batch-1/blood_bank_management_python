from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,  RetrieveUpdateDestroyAPIView
from .models import Register
from .serializers import UserSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
import logging
import random
from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)

class RegisterDetails(ListAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Register.objects.all()
    serializer_class = UserSerializers
    # Retrieves register details request with id and all the register details
    def get(self, request, pk=None):
        if pk is not None:
            register = Register.objects.get(pk=pk)
            serializer = UserSerializers(register)
            logger.info("Register with id {pk} is retrieved")
            return Response(serializer.data)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        logger.info("All Users Retrieved")
        return Response(serializer.data)
    
    # Create a new reister
    def post(self,request):
        serializer=UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        subject = 'People Blood Bank' 
        message = f"Dear {user.first_name},\nThank you for registering on our People Blood Bank!\n We are excited to have you as part of our community. \nIf you have any questions or need assistance, please don't hesitate to reach out to our support team.\n\nHelp Line Numbers :+91-6303247190 , +91-1234567890 \n email : dhanudhanu6303@gmail.com\n\nBest regards,\nPeople Blood Bank"  
        from_email = 'dhanu.django@example.com' 
        recipient_list = [user.email] 
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            logger.info('OTP sent successfully')
            return Response({'message': 'Registration Email sent successfully.', 'user': serializer.data})
        except Exception as e:
            logger.error(f'Failed to send email: {e}')
        return Response({'message': 'Failed to send.'}, status=500)
    
     # update the register details with ID
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # Retrieves the object based on URL parameter
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    def perform_update(self, serializer):
        password = serializer.validated_data.get('password')
        if password:
            instance = serializer.save()
            instance.set_password(password)
            instance.save()
        else:
            serializer.save()

    # Delete register details with ID
    def delete(self, request, pk=None):
        user = self.get_object()
        user.delete()
        logger.info("Register Deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)



class LoginDetails(APIView):
    # Login By using email,password it will generate a token
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        user= Register.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User Not Found')
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        payload={ 
            'id':user.id,
            "iat":datetime.datetime.utcnow(),
            "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=10)
        }
        token=jwt.encode(payload,'secret', algorithm='HS256')
        response=Response()
        serializer = UserSerializers(user)
        # response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
            'user':serializer.data
        }
        return response



class UserDetails(APIView):
    # Retrieves all the details of user using the token
    def get(self, request):
        token = request.headers.get('Authorization')
        # role=request.headers.get('role')
        if not token:
            raise AuthenticationFailed("Not Authorized")
        token = token.split('Bearer ')[1:]
        if not token:
            raise AuthenticationFailed("Invalid token")
        token = token[0]
        try:
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Not Authorized')
        user = Register.objects.filter(id=payload['id']).first()
        if user.role=="user":
            return True
        else:
            return False



class AdminDetails(APIView):
    # Retrieves all the details of admin using the token
    def get(self, request):
        token = request.headers.get('Authorization')
        role=request.headers.get('role')
        if not token:
            raise AuthenticationFailed("Not Authorized")
        token = token.split('Bearer ')[1:]
        if not token:
            raise AuthenticationFailed("Invalid token")
        token = token[0]
        try:
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Not Authorized')
        user = Register.objects.filter(id=payload['id']).first()
        if user.role=="admin":
            return True
        elif user.role=='user':
            return False
        else:
            return True

       

class LogoutView(APIView):
      # Logout using the details
      def post(self,request):
          response=Response()
          response.delete_cookie('jwt')
          response.data={
              'message':'logout success'
          }
          return response
      


