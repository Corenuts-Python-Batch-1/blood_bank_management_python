# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class BloodBank(models.Model):
    blood_bank_id = models.AutoField(primary_key=True)
    blood_bank_name = models.CharField(max_length=45)
    location = models.ForeignKey('Location', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'blood_bank'


class BloodGroup(models.Model):
    blood_group_id = models.AutoField(primary_key=True)
    blood_group_type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'blood_group'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('LoginRegister', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DonarDetails(models.Model):
    donar_id = models.AutoField(primary_key=True)
    donar_name = models.CharField(max_length=45)
    blood_type = models.ForeignKey(BloodGroup, models.DO_NOTHING, db_column='blood_type')
    units = models.IntegerField()
    contact_number = models.BigIntegerField()
    aadhar_number = models.CharField(unique=True, max_length=45)
    transfusion_date = models.DateField()
    eligibility = models.CharField(max_length=45)
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location')

    class Meta:
        managed = False
        db_table = 'donar_details'


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=45)
    area = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'location'


class LoginRegister(models.Model):
    id = models.BigAutoField(primary_key=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=555)
    role = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'login_register'


class LoginRegisterGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    register = models.ForeignKey(LoginRegister, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_register_groups'
        unique_together = (('register', 'group'),)


class LoginRegisterUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    register = models.ForeignKey(LoginRegister, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_register_user_permissions'
        unique_together = (('register', 'permission'),)


class PatientDetails(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    contact_number = models.BigIntegerField()
    blood_group = models.ForeignKey(BloodGroup, models.DO_NOTHING, db_column='blood_group')
    patient_location = models.ForeignKey(Location, models.DO_NOTHING, db_column='patient_location')
    hospital_name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    units_required = models.IntegerField()
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_details'


class TotalUnits(models.Model):
    total_units_id = models.AutoField(primary_key=True)
    blood_type = models.ForeignKey(BloodGroup, models.DO_NOTHING, db_column='blood_type')
    total_units = models.IntegerField()
    blood_bank = models.ForeignKey(BloodBank, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'total_units'
