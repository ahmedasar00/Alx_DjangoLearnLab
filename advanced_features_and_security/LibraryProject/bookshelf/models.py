from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title

#create cumstomer Mangare user 
class customermanageruser(BaseUserManager):
    def create_user(self, email , password = None , **extra_fields):
        if not email:
            raise ValueError("The Eamil field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email **extra_fields)
        user.set_password(password)
        user.save(using =self.db)
        return user
    
    def create_superuser(self , email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        
        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email ,password, **extra_fields)
    



#create Cumstomer User
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    data_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos", null=True, blank=True)
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.emai
    
    