from django.shortcuts import render
from .serializers import *
from Login.models import Register
from Models.models import Location,BloodBank,BloodGroup,TotalUnits,PatientDetails
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.core.mail import send_mail
from datetime import date
from Models.views import *
from rest_framework.views import APIView
import logging
logger = logging.getLogger(__name__)


# Retrieves location by ID or all locations
@api_view(['GET'])
def getLocation(request, location_id=None):
    if location_id is not None:
        try:
            location = Location.objects.get(location_id=location_id)
            serializer = LocationSerializer(location)
            logger.info(f"Location with ID {location_id} retrieved.")
            return Response(serializer.data)
        except Location.DoesNotExist:
            logger.error(f"Location with ID {location_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        qs = Location.objects.all()
        serializer = LocationSerializer(qs, many=True)
        logger.info("Retrieved all locations.")
        return Response(serializer.data)
    
# Creates a new location
@api_view(['POST'])
def createLocation(request):
    if AdminValidated(request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("User location created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Failed to create user location.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Updates an existing location by ID
@api_view(['PUT'])
def updateLocation(request, location_id):
    if AdminValidated(request):
        try:
            location = Location.objects.get(location_id=location_id)
            serializer = LocationSerializer(location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated location with ID: {location_id}")
                return Response(serializer.data)
            else:
                logger.error(f"Failed to update location with ID: {location_id}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            logger.error(f"Location with ID {location_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

# Deletes a location by ID
@api_view(['DELETE'])
def deleteLocation(request, location_id):
    if AdminValidated(request):
        try:
            location = Location.objects.get(location_id=location_id)
            location.delete()
            logger.info(f"Deleted location with ID: {location_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            logger.error(f"Location with ID {location_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)




####Blood Group Crud
# Retrieves Blood Group by ID or all blood groups
@api_view(['GET'])
def getBloodGroup(request, blood_group_id=None):
    if blood_group_id is not None:
        try:
            bloodgroup = BloodGroup.objects.get(blood_group_id=blood_group_id)
            serializer = BloodGroupSerializer(bloodgroup)
            logger.info(f"BloodGroup with ID {blood_group_id} retrieved.") 
            return Response(serializer.data)
        except BloodGroup.DoesNotExist:
            logger.error(f"BloodGroup with ID {blood_group_id} does not exist.") 
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        qs = BloodGroup.objects.all()
        serializer = BloodGroupSerializer(qs, many=True)
        logger.info(f"Retrieved all blood groups.") 
        return Response(serializer.data)
    
# Creates a new blood group
@api_view(['POST'])
def createBloodGroup(request):
    if AdminValidated(request):
        serializer = BloodGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Blood Group Cretaed Successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Blood Group Not Created Invalifd!!!")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Updates an existing blood group by ID
@api_view(['PUT'])
def updateBloodGroup(request, blood_group_id):
    if AdminValidated(request):
        try:
            bloodgroup = BloodGroup.objects.get(blood_group_id=blood_group_id)
            serializer = BloodGroupSerializer(bloodgroup, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Blood Group with ID {blood_group_id} is updated.")
                return Response(serializer.data)
            else:
                logger.error(f"Failed to update Blood Group  with ID: {blood_group_id}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BloodGroup.DoesNotExist:
            logger.error(f"Blood Group  with ID {blood_group_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

# Deletes a blood group by ID
@api_view(['DELETE'])
def deleteBloodGroup(request, blood_group_id):
    if AdminValidated(request):
        try:
            bloodgroup = BloodGroup.objects.get(blood_group_id=blood_group_id)
            bloodgroup.delete()
            logger.info(f"Deleted BloodGroup with ID: {blood_group_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BloodGroup.DoesNotExist:
            logger.error(f"BloodGroup with ID {blood_group_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

# Retrieving Blood Group with location ID and Blood Group ID
@api_view(['GET'])
def getBloodgroupWithLocation(request, location_id=None, blood_group_id=None):
        try:
            blood_group = BloodGroup.objects.get(blood_group_id=blood_group_id)
        except BloodGroup.DoesNotExist:
            logger.error("Blood group does not exist")
            return Response({"error": "Blood group not found"}, status=status.HTTP_404_NOT_FOUND)
        blood_group_type = ""
        total_units = 0
        blood_group_units = {"blood_group_type": blood_group_type, "total_units": total_units}
        if location_id:
            try:
                location = Location.objects.get(location_id=location_id)
                banks = BloodBank.objects.filter(location__city=location.city)
                total_units = TotalUnits.objects.filter(blood_bank__in=banks, blood_type=blood_group).aggregate(total=Sum('total_units'))['total'] or 0
                blood_group_units["blood_group_type"] = str(blood_group.blood_group_type)
                blood_group_units["total_units"] = total_units
                logger.info("Blood Group With Total Units")
                return Response(blood_group_units)
            except Location.DoesNotExist:
                logger.error("Location Not Found")
                return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error("No Units")
            return Response("No Such data")
        

####Blood Bank Crud
# Retrieves Blood Bank by ID or all blood banks
@api_view(['GET'])
def getBloodBank(request, blood_bank_id=None):
    if AdminValidated(request):
        if blood_bank_id is not None:
            try:
                blood_bank = BloodBank.objects.get(blood_bank_id=blood_bank_id)
                serializer = BloodBankSerializer(blood_bank)
                logger.info(f"Blood Bank with ID {blood_bank_id} retrieved.")
                return Response(serializer.data)
            except BloodBank.DoesNotExist:
                logger.error(f"Blood Bank with ID {blood_bank_id} does not exist.")
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            qs = BloodBank.objects.all()
            serializer = BloodBankSerializer(qs, many=True)
            logger.info("Retrieved all blood banks.")
            return Response(serializer.data)
        
# Creates a new blood bank
@api_view(['POST'])
def createBloodBank(request):
    if AdminValidated(request):
        serializer = BloodBankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("BloodBank created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create BloodBank Details.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Updates an existing blood bank by ID
@api_view(['PUT'])
def updateBloodBank(request, blood_bank_id):
    if AdminValidated(request):
        try:
            bloodbank = BloodBank.objects.get(blood_bank_id=blood_bank_id)
            serializer = BloodBankSerializer(bloodbank, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated BloodBank with ID: {blood_bank_id}")
                return Response(serializer.data)
            logger.error(f"Failed to update BloodBank with ID: {blood_bank_id}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BloodBank.DoesNotExist:
            logger.error(f"BloodBank with ID {blood_bank_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

# Deletes a blood bank by ID
@api_view(['DELETE'])
def deleteBloodBank(request, blood_bank_id):
    if AdminValidated(request):
        try:
            patient = BloodBank.objects.get(blood_bank_id=blood_bank_id)
            patient.delete()
            logger.info(f"Deleted BloodBank with ID: {blood_bank_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BloodBank.DoesNotExist:
            logger.error(f"BloodBank with ID {blood_bank_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)
        


####Patient Crud
# Retrieves Patient Details by ID or all patient details
@api_view(['GET'])
def getPatientDetails(request, patient_id=None):
    if AdminValidated(request):
        if patient_id is not None:
            try:
                patient = PatientDetails.objects.get(patient_id=patient_id)
                serializer = PatientSerializer(patient)  
                logger.info(f" PatientDetails with ID {patient_id} retrieved.")
                return Response(serializer.data)
            except PatientDetails.DoesNotExist:
                logger.error(f"PatientDetails with ID {patient_id} does not exist.")
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            qs = PatientDetails.objects.all()
            serializer = PatientSerializer(qs, many=True)
            logger.info("Retrieved all requested Patients")
            return Response(serializer.data)
        
# Create a patient details 
@api_view(['POST'])
def createPatientDetails(request):
    if UserValidated(request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Patient created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create Patient Details.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update the patient details with the given ID
@api_view(['PUT'])
def updatePatientDetails(request, patient_id):
    if UserValidated(request):
        try:
            patient = PatientDetails.objects.get(patient_id=patient_id)
            serializer = PatientSerializer(patient, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated PatientDetails with ID: {patient_id}")
                return Response(serializer.data)
            logger.error(f"Failed to update PatientDetails with ID: {patient_id}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PatientDetails.DoesNotExist:
            logger.error(f"PatientDetails with ID {patient_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

# Deletes a patient details by ID
@api_view(['DELETE'])
def deletePatientDetails(request, patient_id):
    if AdminValidated(request):
        try:
            patient = PatientDetails.objects.get(patient_id=patient_id)
            patient.delete()
            logger.info(f"Deleted PatientDetails with ID: {patient_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PatientDetails.DoesNotExist:
            logger.error(f"PatientDetails with ID {patient_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)
        

@api_view(['GET'])
def currentDayAllRequestsPatientDetails(request):
    if AdminValidated(request):
        try:
            current_date = date.today()
            patient_details = PatientDetails.objects.filter(created_at=current_date)
            serializer = PatientSerializer(patient_details, many=True)
            logger.info("Present Day Requested Patients")
            return Response(serializer.data)
        except PatientDetails.DoesNotExist:
            logger.error("No Patient Requests Today!")
            return Response(status=status.HTTP_404_NOT_FOUND)
# Retrieves current day requests of patientdetails
@api_view(['GET'])
def currentDayRequestedPatientDetails(request):
    if AdminValidated(request):
        try:
            current_date = date.today()
            patient_details = PatientDetails.objects.filter(created_at=current_date, status='requested')
            serializer = PatientSerializer(patient_details, many=True)
            logger.info("Present Day Requested Patients")
            return Response(serializer.data)
        except PatientDetails.DoesNotExist:
            logger.error("No Patient Requests Today!")
            return Response(status=status.HTTP_404_NOT_FOUND)
         
# Retrieves all pending requests of patientdetails
@api_view(['GET'])
def getRequestedPatientsByLocation(request, location_id):
    if AdminValidated(request):
        try:
            location = Location.objects.get(location_id=location_id)
            requested_patients = PatientDetails.objects.filter(patient_location=location, status='requested')
            serializer = PatientSerializer(requested_patients, many=True)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)

# Retrieves current day accepted requests of patientdetails
@api_view(['GET'])
def currentDayAcceptedPatientDetails(request):
    if AdminValidated(request):
        try:
            current_date = date.today()
            patient_details = PatientDetails.objects.filter(created_at=current_date,status='accepted')
            serializer = PatientSerializer(patient_details, many=True)
            logger.info("Present Day Request Accepted Patients")
            return Response(serializer.data)
        except PatientDetails.DoesNotExist:
            logger.error(f"No Patient Request Accepted Today!!.")
            return Response(status=status.HTTP_404_NOT_FOUND)   


              
####Total Units Crud
# Retrieves Total Units by ID or all total units
@api_view(['GET'])
def getTotalUnits(request, total_units_id=None):
    if AdminValidated(request):
        if total_units_id is not None:
            try:
                t_units = TotalUnits.objects.get(total_units_id=total_units_id)
                serializer = TotalUnitsSerializer(t_units) 
                logger.info(f" TotalUnits with ID {total_units_id} retrieved.")
                return Response(serializer.data)
            except TotalUnits.DoesNotExist:
                logger.error(f"TotalUnits with ID {total_units_id} does not exist.")
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            qs = TotalUnits.objects.all()
            serializer = TotalUnitsSerializer(qs, many=True)
            logger.info("Retrieved all TotalUnits.")
            return Response(serializer.data)

# Creates a new total units
@api_view(['POST'])
def createTotalUnits(request):
    serializer = TotalUnitsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info("Total Units created successfully.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.error("Failed to create total units.")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Updates an existing total units by ID
@api_view(['PUT'])
def updateTotalUnits(request, total_units_id):
    if AdminValidated(request):
        try:
            patient = TotalUnits.objects.get(total_units_id=total_units_id)
            serializer = TotalUnitsSerializer(patient, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated Total units with ID: {total_units_id}")
                return Response(serializer.data)
            else:
                logger.error(f"Failed to update Total Units with ID: {total_units_id}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TotalUnits.DoesNotExist:
            logger.error(f"Total Units with ID {total_units_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

# Deletes a total units by ID
@api_view(['DELETE'])
def deleteTotalUnits(request, total_units_id):
    if AdminValidated(request):
        try:
            total_units = TotalUnits.objects.get(total_units_id=total_units_id)
            total_units.delete()
            logger.info(f"Deleted Total Units with ID: {total_units_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TotalUnits.DoesNotExist:
            logger.error(f"Total Units with ID {total_units_id} does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

# Retrieving blood group along with total units using location ID
@api_view(['GET'])
def getBloodGroupWithTotalUnits(request, location_id=None):
    if AdminValidated(request):
        blood_groups = BloodGroup.objects.all()
        blood_group_units = {}
        if location_id is not None:
            try:
                banks = BloodBank.objects.filter(location_id=location_id)
                totalBigunits = TotalUnits.objects.filter(blood_bank__in=banks)
                serializer = TotalUnitsSerializer(totalBigunits,many = True)
                for blood_group in blood_groups:
                    bloodtype = totalBigunits.filter(blood_type=blood_group)
                    total_units = bloodtype.aggregate(total=Sum('total_units'))['total'] or 0
                    blood_group_units[blood_group.blood_group_type] = total_units
                logger.info("Blood Group With Units")
                return Response(serializer.data)
            except BloodBank.DoesNotExist:
                logger.error("Blood Group Does not exist")
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error("No Units")
            return Response("No Such data")

@api_view(['GET'])
def getTotalUnitsByBloodGroup(request):
    if AdminValidated(request):
        blood_group_totals = TotalUnits.objects.values('blood_type__blood_group_type').annotate(total_units=Sum('total_units'))
        blood_group_data = []
        for blood_group_total in blood_group_totals:
            blood_group_type = blood_group_total['blood_type__blood_group_type']
            total_units = blood_group_total['total_units']
            blood_group_data.append({'blood_group_type': blood_group_type, 'total_units': total_units})
        return Response(blood_group_data)
    
@api_view(["PUT"])
def patientAccept(request, patient_id=None):
    try:
        patient=PatientDetails.objects.get(pk=patient_id)
       
    except PatientDetails.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
    req = patient.units_required

   
    try:
        # blood_group = BloodGroup.objects.get(blood_group_type=patient.blood_group)
         blood_banks = BloodBank.objects.filter(location=patient.patient_location)
    except BloodGroup.DoesNotExist:
        return Response({"error": "Blood group not found"}, status=status.HTTP_404_NOT_FOUND)
    total_units = TotalUnits.objects.filter(blood_bank__in=blood_banks, blood_type=patient.blood_group)
    for unit in total_units:
        if req <= unit.total_units and req > 0:
            unit.total_units -= req
            unit.save()
            break
        elif req > 0:
            req -= unit.total_units
            unit.total_units = 0
            unit.save()
    patient.status = "accepted"
    patient.save()

    serializer = PatientSerializer(patient)
    return Response(serializer.data)
@api_view(["PATCH"])
def patientReject(request, patient_id=None):
    try:
        patient = PatientDetails.objects.get(pk=patient_id)
        patient.status = "rejected"
        patient.save()
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    except PatientDetails.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)