from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import uuid

# CustomManager
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
    

# CustomUser
class CustomUser(AbstractBaseUser, PermissionsMixin):

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
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} and email: {self.email}"

# Profile
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sellerprofile")
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)


# ProductCategory
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

# Product
class Product(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="products_pics/", blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    category = models.ManyToManyField(ProductCategory, related_name="products")
    quantity = models.IntegerField()

# Rating 
class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name="ratings")
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # who gave the rating
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Post
class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    picture = models.ImageField(upload_to="post_picture/", null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

# User_session
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="usersessions", on_delete=models.CASCADE)
    session_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name
