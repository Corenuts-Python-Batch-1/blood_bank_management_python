from rest_framework.serializers import ModelSerializer
from Models.models import Location,BloodBank,BloodGroup,PatientDetails,TotalUnits
from rest_framework import serializers


class LocationSerializer(ModelSerializer):
    class Meta:
        model=Location
        fields='__all__'



class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodGroup
        fields = ['blood_group_id', 'blood_group_type']



class PatientSerializer(ModelSerializer):
    patient_location = LocationSerializer()  
    blood_group = BloodGroupSerializer()  
    class Meta:
        model = PatientDetails
        fields = '__all__'
    def create(self, validated_data):
        patient_location_data = validated_data.pop('patient_location')
        blood_group_data = validated_data.pop('blood_group')
        patient_location = Location.objects.filter(**patient_location_data).first()
        if not patient_location:
                patient_location = Location.objects.create(**patient_location_data)
        blood_group = BloodGroup.objects.filter(**blood_group_data).first()
        if not blood_group:
            blood_group = BloodGroup.objects.create(**blood_group_data)
        patient = PatientDetails.objects.create(
            patient_location=patient_location,
            blood_group =blood_group,
            **validated_data
        )
        return patient
    
    def update(self, instance, validated_data):
        patient_location_data = validated_data.pop('patient_location')
        blood_group_data = validated_data.pop('blood_group')
        print(blood_group_data)
        patient_location = instance.patient_location
        if patient_location:
            patient_location.city = patient_location_data.get('city', patient_location.city)
            patient_location.area = patient_location_data.get('area', patient_location.area)
            patient_location.save()
        else:
            patient_location = Location.objects.create(**patient_location_data)
        blood_group = instance.blood_group
        if blood_group:
            blood_group.group_type = blood_group_data.get('blood_group_type', blood_group.blood_group_type)
            blood_group.save()
        else:
            blood_group = BloodGroup.objects.create(**blood_group_data)
        instance.patient_location = patient_location
        instance.blood_group = blood_group
        instance.patient_name = validated_data.get('patient_name', instance.patient_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.hospital_name = validated_data.get('hospital_name', instance.hospital_name)
        instance.status = validated_data.get('status', instance.status)
        instance.units_required = validated_data.get('units_required', instance.units_required)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()



class BloodBankSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = BloodBank
        fields = ['blood_bank_id', 'blood_bank_name', 'location']
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.filter(**location_data).first()
        if not location:
                location = Location.objects.create(**location_data)
        locationdata = BloodBank.objects.create(
            location=location,
            **validated_data
        )
        return locationdata
    
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location')
        location = instance.location
        if location:
            location.city = location_data.get('city', location.city)
            location.area = location_data.get('area', location.area)
            location.save()
        else:
            location = Location.objects.create(**location_data)
        instance.location = location
        instance.blood_bank_name = validated_data.get('blood_bank_name', instance.blood_bank_name)
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()

        

class TotalUnitsSerializer(serializers.ModelSerializer):
    blood_type = BloodGroupSerializer()
    blood_bank = BloodBankSerializer()
    class Meta:
        model = TotalUnits
        fields = ['total_units_id', 'blood_type', 'total_units', 'blood_bank']
    def create(self, validated_data):
        blood_bank_data = validated_data.pop('blood_bank')
        blood_type_data = validated_data.pop('blood_type')
        location_data = blood_bank_data.pop('location')
        location = Location.objects.get(**location_data)
        blood_bank = BloodBank.objects.get(location=location, **blood_bank_data)
        blood_type = BloodGroup.objects.get(**blood_type_data)
        total_units = TotalUnits.objects.create(blood_bank=blood_bank, blood_type=blood_type, **validated_data)
        return total_units
    
    def update(self, instance, validated_data):
        blood_bank_data = validated_data.pop('blood_bank', {})
        blood_type_data = validated_data.pop('blood_type', {})
        if 'location' in blood_bank_data:
            location_data = blood_bank_data.pop('location')
            location = Location.objects.get(**location_data)
            instance.blood_bank.location = location
        for key, value in blood_bank_data.items():
            setattr(instance.blood_bank, key, value)
        for key, value in blood_type_data.items():
            setattr(instance.blood_type, key, value)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.blood_bank.save()
        instance.blood_type.save()
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.blood_bank.delete()
        instance.blood_type.delete()
        instance.delete()








        

 
    


       


