from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



class MyUserManager(BaseUserManager):
    def create_user(self,email,phone_number,first_name,last_name, password=None,**extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        print("++++++++++++")
        print("create user called")
        print(phone_number)
        if not phone_number:
            raise ValueError("Users must have an phone number")
        
        if not first_name:
            raise ValueError("Users must have an first name")
        
        if not last_name:
            raise ValueError("Users must have an last name")
        
        if not email:
            raise ValueError("Users must have an last name")
        
        
        # user = None
        # if extra_fields.get('email'):

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            middle_name = extra_fields.get('midle_name'),
            address = extra_fields.get('address')
        )
        # else:
        #     user = self.model(
        #         first_name=first_name,
        #         last_name=last_name,
        #         phone_number=phone_number,
        #         password=password,  
        #         **extra_fields
        #     )
            

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,phone_number,first_name,last_name, password,**extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        print("create sup called")
        print("email")
        user = self.create_user(
            email = email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
            
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(_("first name"),max_length=40)
    middle_name = models.CharField(_("middle name"),max_length=40,blank=True,null=True)
    last_name = models.CharField(_("last name"),max_length=40)
    email = models.EmailField(_("email"),max_length=200,unique=True,blank=True,null=True)
    phone_number = models.IntegerField(_("phone number"),unique=True)
    is_email_verified = models.BooleanField(_("email verified"),default=False)
    address = models.CharField(_("address"),max_length=100,blank=True,null=True)
    has_verified_dairy = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    def __str__(self):
        return self.get_name()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","phone_number"]

    objects = MyUserManager()

    def get_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    
    

