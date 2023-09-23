from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from app.custom_manager import CustomUserManager
from app.model_manager import CollectionManager
# Create your models here.

class BaseModel(models.Model):
    """
    Data required in every table is created in this model and inherited by below models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class User(PermissionsMixin, AbstractBaseUser, BaseModel):
    """
    User model stores all user related information.
    """

    id = models.BigAutoField(primary_key=True)
    user_ting = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    # status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Genre(BaseModel):
    name = models.CharField(max_length=255)


    class Meta:
        db_table = "genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Movie(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    uuid = models.UUIDField()


    class Meta:
        # unique_together = ('uuid')
        db_table = "movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title


class Collection(BaseModel):
    """
    Collection model stores all Collection related information.
    """

    title = models.CharField(max_length=255)
    collection_ting = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField('Movie', related_name='collections')
    
    objects = models.Manager()  
    active_collections = CollectionManager() 

    class Meta:
        unique_together = ('user', 'title')
        db_table = "collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.title
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()


class RequestCount(BaseModel):
    count = models.PositiveIntegerField(default=0)
    

    class Meta:
        db_table = "request_count"
        verbose_name_plural = "RequestCounts"

    def __str__(self):
        return self.count
    

