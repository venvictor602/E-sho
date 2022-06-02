from django.db import models
from  django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name= models.CharField(max_length=200,null=True,blank=True)
    previous_price=models.DecimalField(max_digits=7,decimal_places=2)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url = ""
        return url

class Order(models.Model):
    customer=models.ForeignKey(Customer,null=True,blank=True,on_delete=models.SET_NULL)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping=False
        orderitems= self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping= True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,null=True,blank=True,on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,null=True,blank=True,on_delete=models.SET_NULL)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address    

People = (
    ('1 person','1 PERSON'),
    ('2 person','2 PERSON'),
    ('3 person','3 PERSON'),
    ('4+ person','4+ PERSON'),
)

class Reservation(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    people=models.CharField(max_length=200,choices=People)
    phone=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    time=models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email
