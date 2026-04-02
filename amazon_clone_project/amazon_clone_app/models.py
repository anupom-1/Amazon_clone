from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomManager(BaseUserManager):

    def _create_user(self, email = None, password = None, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_user(self, email = None, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email = None, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("The superuser must be set 'is_staff' is True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("The superuser must be set 'is_superuser' is True")
        
        return self._create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    class AccountChoices(models.TextChoices):
        Seller = "S", "Seller"
        Buyer = "B", "Buyer"
    
    class GenderChoices(models.TextChoices):
        Male = "M", "Male"
        Female = "F", "Female"
        Other = "O", "Other"

    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    account_type = models.CharField(max_length=1, choices=AccountChoices.choices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} and email: {self.email}"

    