from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
# custom account manager
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None,):
        if not email:
            raise ValueError ("Users must have an email address")
        
        if not username:
            raise ValueError ("Users must have a username")
        
        user = self.model(
            email        = self.normalize_email(email),
            username     = username,
            first_name   = first_name,
            last_name    = last_name,
            phone_number = phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, phone_number, password=None,):
        user = self.create_user(
            email        = self.normalize_email(email),
            username     = username,
            first_name   = first_name,
            last_name    = last_name,
            phone_number = phone_number,
            password     = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user

# Account model
class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, verbose_name="First name")
    last_name = models.CharField(max_length=50, verbose_name="Last name")
    username = models.CharField(max_length=50, unique=True, verbose_name="Username")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=50, unique=True, verbose_name="Phone number")

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True) # the date the user created the account wont update
    last_login = models.DateTimeField(auto_now=True)    # the date the user last logged in will update
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False) 


    USERNAME_FIELD = 'email' # the email field will be used as the username field
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number'] # the required fields for creating a user

    objects = MyAccountManager() # connect the MyAccountManager class to the Account model

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None): # Uses Django's built-in permission logic
        return self.is_admin
    
    def has_module_perms(self, app_label): # Superusers have all permissions
        return True