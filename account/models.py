from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


GENDER_CHOICE = (
    ('M','Male'),
    ('F','Female'),
    ('O','Others')
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Profile(models.Model):
    avatar = models.ImageField(upload_to='profile',blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profiles')
    address = models.CharField(max_length=255,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    gender = models.CharField(choices=GENDER_CHOICE,max_length=128,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.user.email
    

class Follow(models.Model):
    youser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name = 'account')
    follow = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_info')

    def __str__(self):
        return f"{self.youser.email} -> {self.follow.email}"

