from django.db import models

# Create your models here.
class Product(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Price = models.DecimalField(max_digits=6, decimal_places=2)
    Inventory = models.IntegerField()
    Last_Update = models.DateTimeField(auto_now=True)

class Customer(models.Model):
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, 'Gole'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_BRONZE, 'Bronze'),
    ]
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=20)
    Birth_Date = models.DateField(null=True)
    Membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

class Order(models.Model):
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    Placed_At = models.DateTimeField(auto_now_add=True)
    Payment_Status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)