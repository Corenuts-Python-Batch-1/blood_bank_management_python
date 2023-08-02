from django.db import models
from django.contrib.auth.models import AbstractUser
class Register(AbstractUser):
    email = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)
    role = models.CharField(max_length=45,default='user')
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username=None
    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'

    class Meta:
        managed = False
        db_table = 'login_register'
