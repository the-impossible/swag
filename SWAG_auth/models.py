from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse
import uuid
from datetime import datetime
# My app imports

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, password=None):

        # creates a user with the parameters
        if email is None:
            raise ValueError('Email address is required!')

        if name is None:
            raise ValueError('Full name is required!')

        if phone_number is None:
            raise ValueError('Phone number is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
            name=name.title().strip(),
            phone_number = phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, phone_number, password=None):
        # create a superuser with the above parameters

        user = self.create_user(
            email=email,
            name=name,
            phone_number=phone_number,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    name = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    phone_number = PhoneNumberField(db_index=True, unique=True, blank=True)
    picture = models.ImageField(
        default='img/user.png', upload_to='uploads/', null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(to="SWAG_payment.States", null=True, blank=True, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_updated(self):
        if self.state != None:
            return True
        return False

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("auth:profile", kwargs={
            'pk': self.user_id
        })

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'
