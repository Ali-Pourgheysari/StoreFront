from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Promotion(models.Model):
    description: models.CharField(max_length=255)
    discount = models.FloatField()
    
class Collection(models.Model):
    title = models.CharField(max_length=100)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    #setting:
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
        
class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion, blank=True)

    #setting:
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, 'Gole'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_BRONZE, 'Bronze'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    #setting:
    def __str__(self) -> str:
        return self.first_name + self.last_name

class Order(models.Model):
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_At = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT) 
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveBigIntegerField()
    order = models.ForeignKey(Order, on_delete=models.PROTECT) 

class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip = models.PositiveBigIntegerField()
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    quantity = models.PositiveBigIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 