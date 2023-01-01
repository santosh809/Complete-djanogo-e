# Create your models here.
from django.contrib.auth.models import User
from time import timezone
from tkinter import CASCADE
from django.db import models
# from Ckeditor.Field import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
# from django_countries_field import CountryField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__ (self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField( blank = True)
    image = models.ImageField(upload_to = 'media')
    slug = models.CharField(max_length=100)

    def __str__ (self):
        return self.name

class Ads(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'media')
    slug = models.CharField(max_length=100)
    rank = models.IntegerField()

    def __str__ (self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'media')
    slug = models.CharField(max_length=100)
    rank = models.IntegerField(unique=True)

    def __str__ (self):
        return self.name


STOCK = (('in stock', 'in stock'),('out stock' ,'out stock'))
LABEL = (('hot','hot'),('new','new'),('sale','sale'))
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    stock = models.CharField(choices=STOCK, max_length=100)
    label = models.CharField(choices=LABEL, max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'media')
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, blank=True)
    specifacation = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)

    def __str__ (self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'media')
    profession = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100)

    def __str__ (self):
        return self.name 

class Cart(models.Model):
    username = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    quentity = models.PositiveIntegerField(default = 1)
    total = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    checkout = models.BooleanField(default = False)
    items = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username

class Comment(models.Model):
    username = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    rate = models.CharField(max_length=5)
    date = models.DateField(default=timezone.now)
    Comment = models.TextField()

    def __str__(self):
        return str(self.date)

class Like(models.Model):
    username = models.CharField(max_length=150)
    slug = models.CharField(max_length=100)
    total = models.IntegerField(default=0)
    items = models.ForeignKey(Product,on_delete=models.CASCADE)
 
    def __str__(self):
        return self.username

#----------------------------------------------Checkout----------------------
class CheckOut(models.Model):
    username = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    zip_code = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()

    def __str__(self):
        return self.username
#-----------------------------------------Profile----------------------------------------
class Profile ( models.Model ) :
    user = models.OneToOneField(User, on_delete=models . CASCADE )
    forget_password_token = models.CharField (max_length = 100 )
    created_at = models.DateTimeField(auto_now_add = True)

    
    def _str_ ( self ) :
        return str(self.created_at)