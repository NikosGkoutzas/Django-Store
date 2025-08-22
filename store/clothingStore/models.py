from django.db import models
from django.contrib.auth.models import User

##     NA BALW META ANDRIKA/GUNAIKEIA ##

SIZE_CHOICES = [
             ('Extra small' , 'XS') , 
             ('Small' , 'S') , 
             ('Medium' , 'M') , 
             ('Large' , 'L') , 
             ('Extra large' , 'XL')
             ]


# The category of clothes
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300 , blank=True , null=True)

    def __str__(self):
        return self.name



# The actual object
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500 , blank=True , null=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20 , choices=SIZE_CHOICES , default='XS')
    category = models.ForeignKey(Category , on_delete=models.CASCADE , blank=False , null=False)


    def __str__(self):
        return self.name
    


# Products in shopping cart
class CartItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='items')
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=20 , choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.product.name} ({self.product.size}) x {self.quantity}"
        


class Order(models.Model):
    items = models.ManyToManyField(CartItem , related_name='orders')  
    customer = models.ForeignKey(User , on_delete=models.CASCADE , related_name='orders' , null=True , blank=True)
    status_choices = [
             ('PENDING' , 'Pending') , 
             ('PAID' , 'Paid') , 
             ('SHIPPED' , 'Shipped') , 
             ('CANCELLED' , 'Cancelled') , 
             ]
    status = models.CharField(max_length=20 , choices=status_choices , default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} status: {self.status}"
    

