from rest_framework.serializers import ModelSerializer
from Models.models import DonarDetails,Location,BloodGroup
from rest_framework import serializers
from UserView.serializers import *


class DonarSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    blood_type = BloodGroupSerializer()
    bank = BloodBankSerializer()

    class Meta:
        model = DonarDetails
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['transfusion_date'] = instance.transfusion_date.strftime("%d/%m/%Y")
        return representation
    def create(self, validated_data):
            location_data = validated_data.pop('location')
            blood_type_data = validated_data.pop('blood_type')
            bank_data = validated_data.pop('bank')
            location_data_one = bank_data.pop('location')
            location = Location.objects.get(**location_data_one)
            location = Location.objects.get(**location_data)
            blood_type = BloodGroup.objects.get(**blood_type_data)
            bank = BloodBank.objects.get(location = location,**bank_data)

            donor = DonarDetails.objects.create(
                location=location,
                blood_type=blood_type,
                bank=bank,
                **validated_data
            )
            return donor  
    
    #  def update(self, instance, validated_data):
    #         blood_bank_data = validated_data.pop('blood_bank', {})
    #     blood_type_data = validated_data.pop('blood_type', {})
    #     if 'location' in blood_bank_data:
    #         location_data = blood_bank_data.pop('location')
    #         location = Location.objects.get(**location_data)
    #         instance.blood_bank.location = location
    #     for key, value in blood_bank_data.items():
    #         setattr(instance.blood_bank, key, value)
    #     for key, value in blood_type_data.items():
    #         setattr(instance.blood_type, key, value)
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.blood_bank.save()
    #     instance.blood_type.save()
    #     instance.save()
    #     return instance
                 
    # def update(self, instance, validated_data):
    #     location_data = validated_data.pop('location', {})
    #     blood_type_data = validated_data.pop('blood_type',{})
    #     bank_data = validated_data.pop('bank',{})
    #     location = instance.location
    #     if location:
    #         location.city = location_data.get('city', location.city)
    #         location.area = location_data.get('area', location.area)
    #         location.save()
    #     else:
    #         location = Location.objects.create(**location_data)
    #     blood_type = instance.blood_type
    #     if blood_type:
    #         blood_type.blood_group_type = blood_type_data.get('blood_group_type', blood_type.blood_group_type)
    #         blood_type.save()
    #     else:
    #         blood_type = BloodGroup.objects.create(**blood_type_data)
    #     instance.location = location
    #     instance.blood_type = blood_type
    #     instance.donar_name = validated_data.get('donar_name', instance.donar_name)
    #     instance.units = validated_data.get('units', instance.units)
    #     instance.aadhar_number = validated_data.get('aadhar_number', instance.aadhar_number)
    #     instance.contact_number = validated_data.get('contact_number', instance.contact_number)
    #     instance.transfusion_date = validated_data.get('transfusion_date', instance.transfusion_date)
    #     instance.eligibility = validated_data.get('eligibility', instance.eligibility)
    #     instance.save()
    #     return instance


    # def update(self, instance, validated_data):
    #     location_data = validated_data.pop('location')
    #     blood_type_data = validated_data.pop('blood_type')
    #     bank_data = validated_data.pop('bank')
        
    #     # Retrieve the existing related objects
    #     location = instance.location
    #     blood_type = instance.blood_type
    #     bank = instance.bank
        
    #     # Update the related objects if provided in the validated data
    #     if location_data:
    #         location_serializer = LocationSerializer(location, data=location_data)
    #         location_serializer.is_valid(raise_exception=True)
    #         location = location_serializer.save()
        
    #     if blood_type_data:
    #         blood_type = BloodGroup.objects.get(**blood_type_data)
        
    #     if bank_data:
    #         bank = BloodBank.objects.get(location=location, **bank_data)
        
    #     # Update the instance fields
    #     instance.location = location
    #     instance.blood_type = blood_type
    #     instance.bank = bank
        
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
        
    #     instance.save()
    #     return instance



    def delete(self, instance):
        instance.delete()