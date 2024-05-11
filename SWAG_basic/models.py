from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Role(models.Model):
    role = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.role}'

    class Meta:
        db_table = 'Role'
        verbose_name_plural = "Role"

class Gender(models.Model):
    gender = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.gender}'

    class Meta:
        db_table = 'Gender'
        verbose_name_plural = "Gender"

class Volunteer(models.Model):
    volunteer_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    phone_number = PhoneNumberField(db_index=True, unique=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    occupation = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    age = models.CharField(
        max_length=2, db_index=True, blank=True, null=True)
    role_you_want_to_volunteer = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    other_role = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    school = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name='date_created', auto_now=True, null=True)

    def __str__(self):
        return f'{self.name} | {self.email}, is volunteering'


    class Meta:
        db_table = 'Volunteer'
        verbose_name_plural = "Volunteers"

class Training(models.Model):

    training_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    phone_number = PhoneNumberField(db_index=True, unique=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    occupation = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    age = models.CharField(
        max_length=2, db_index=True, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name='date_created', auto_now=True, null=True)


    def __str__(self):
        return f'{self.name} | {self.email}, is registering for Training'


    class Meta:
        db_table = 'Training'
        verbose_name_plural = "Trainings"

