from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from Models.views import *
from django.db import transaction
import logging
logger = logging.getLogger(__name__)

# Donor Details Crud OPerations
# Retrieves the donor details by ID or all the donor details and count of the donors
@api_view(['GET'])
def getDonorDetails(request, donar_id=None):
    try:
        if AdminValidated(request):
            if donar_id is not None:
                try:
                    location = DonarDetails.objects.get(donar_id=donar_id)
                    serializer = DonarSerializer(location) 
                    print(serializer) 
                    logger.info(f"DonarDetails with ID {donar_id} retrieved.") 
                    return Response(serializer.data)
                except DonarDetails.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                qs = DonarDetails.objects.all()
                serializer = DonarSerializer(qs, many=True)
                logger.info("Present Day Donors")
                return Response(serializer.data)
    except Exception as e:
        logger.error(f"An error occurred while retrieving donor details: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Create a new donor detail and update the total units of the given blood group in the blood bank
@api_view(['POST'])
def createDonorDetails(request):
    try:


        serializer = DonarSerializer(data=request.data)

        if serializer.is_valid():
            with transaction.atomic():
                donor = serializer.save()
                total = TotalUnits.objects.filter(blood_type=donor.blood_type, blood_bank=donor.bank).first()
                if total is not None:
                    total.total_units += donor.units
                    total.save()
                else:
                    TotalUnits.objects.create(
                        blood_type=donor.blood_type,
                        blood_bank=donor.bank,
                        total_units=donor.units
                    )
                logger.info("Donor created successfully.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create Donor.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"An error occurred while creating donor details: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update the donor details by using ID
@api_view(['PUT'])
def updateDonorDetails(request, donar_id):
    try:
        if AdminValidated(request):
            try:
                donor = DonarDetails.objects.get(donar_id=donar_id)
                serializer = DonarSerializer(donor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"Updated DonarDetails with ID: {donar_id}")
                    return Response(serializer.data)
                logger.error(f"Failed to update DonarDetails with ID: {donar_id}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except DonarDetails.DoesNotExist:
                logger.error(f"DonarDetails with ID {donar_id} does not exist.")
                return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"An error occurred while updating donor details: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete the Donor Details by ID
@api_view(['DELETE'])
def deleteDonorDetails(request, donar_id):
    try:
        if AdminValidated(request):
            try:
                donor = DonarDetails.objects.get(donar_id=donar_id)
                donor.delete()
                logger.info(f"Deleted DonarDetails with ID: {donar_id}")
                return Response(status=status.HTTP_204_NO_CONTENT)
            except DonarDetails.DoesNotExist:
                logger.error(f"DonarDetails with ID {donar_id} does not exist.")
                return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"An error occurred while deleting donor details: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Retrieve the current day donors
@api_view(['GET'])
def currentDayDonorDetails(request):
    try:
        if AdminValidated(request):
            try:
                current_date = date.today()
                donor_details = DonarDetails.objects.filter(transfusion_date=current_date)
                serializer = DonarSerializer(donor_details, many=True)
                logger.info("Present Day Donors")
                return Response(serializer.data)
            except:
                logger.error(f"No Donors Today!!.")
                return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"An error occurred while retrieving current day donor details: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['GET'])
# def totalBlood(request):
#     if AdminValidated(request):

        
# @api_view(['GET'])
# def getBloodGroupWithTotalUnits(request, location_id=None):
#     if AdminValidated(request):
#         blood_groups = BloodGroup.objects.all()
#         blood_group_units = {}
#         if location_id is not None:
#             try:
#                 banks = BloodBank.objects.filter(location_id=location_id)
#                 totalBigunits = TotalUnits.objects.filter(blood_bank__in=banks)
#                 serializer = TotalUnitsSerializer(totalBigunits,many = True)
#                 for blood_group in blood_groups:
#                     bloodtype = totalBigunits.filter(blood_type=blood_group)
#                     total_units = bloodtype.aggregate(total=Sum('total_units'))['total'] or 0
#                     blood_group_units[blood_group.blood_group_type] = total_units
#                 logger.info("Blood Group With Units")
#                 return Response(serializer.data)
#             except BloodBank.DoesNotExist:
#                 logger.error("Blood Group Does not exist")
#                 return Response(status=status.HTTP_404_NOT_FOUND)
#         else:
#             logger.error("No Units")
#             return Response("No Such data")