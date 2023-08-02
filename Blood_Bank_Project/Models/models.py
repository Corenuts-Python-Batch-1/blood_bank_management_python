from django.db import models
from datetime import date
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=45)
    area = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'location'


class BloodGroup(models.Model):
    blood_group_id = models.AutoField(primary_key=True)
    blood_group_type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'blood_group'

    

class PatientDetails(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    contact_number = models.BigIntegerField()
    blood_group = models.ForeignKey(BloodGroup, models.DO_NOTHING, db_column='blood_group')
    patient_location = models.ForeignKey(Location, models.DO_NOTHING, db_column='patient_location')
    hospital_name = models.CharField(max_length=45)
    status = models.CharField(max_length=45,default='requested')
    units_required = models.IntegerField()
    age = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(default=date.today) 

    class Meta:
        managed = False
        db_table = 'patient_details'


class BloodBank(models.Model):
    blood_bank_id = models.AutoField(primary_key=True)
    blood_bank_name = models.CharField(max_length=45)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    

    class Meta:
        managed = False
        db_table = 'blood_bank'



class TotalUnits(models.Model):
    total_units_id = models.AutoField(primary_key=True)
    blood_type = models.ForeignKey(BloodGroup, models.DO_NOTHING, db_column='blood_type')
    total_units = models.IntegerField()
    blood_bank = models.ForeignKey(BloodBank, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'total_units'


class DonarDetails(models.Model):
    donar_id = models.AutoField(primary_key=True)
    donar_name = models.CharField(max_length=45)
    blood_type = models.ForeignKey(BloodGroup, models.DO_NOTHING, db_column='blood_type')
    units = models.IntegerField()
    contact_number = models.BigIntegerField()
    aadhar_number = models.CharField(unique=True, max_length=45)
    transfusion_date = models.DateField(default=date.today) 
    eligibility = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    age = models.IntegerField()
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='location')
    bank=models.ForeignKey(BloodBank,models.DO_NOTHING,db_column='bank')

    class Meta:
        managed = False
        db_table = 'donar_details'

