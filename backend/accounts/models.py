from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, full_Name,tc, password=None, password2=None):
        """
        Creates and saves a User with the given email, full_Name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            full_Name=full_Name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_Name,tc, password=None):
        """
        Creates and saves a superuser with the given email, full_Name ,   and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_Name=full_Name,

            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    full_Name=models.CharField(verbose_name="Full Name", max_length=255)

    email = models.EmailField(verbose_name="Email",max_length=255,unique=True,)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    tc=models.BooleanField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_Name','tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin 

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
