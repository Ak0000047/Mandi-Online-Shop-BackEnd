from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.




class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name







class MandiMenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    image= models.ImageField(upload_to='images',blank=True,null=True)
    availability = models.BooleanField(default=True)
    
    @property
    def reviews(self):
        return Review.objects.filter(item=self)

    def __str__(self) -> str:
        return self.item_name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(MandiMenuItem,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)



class Order(models.Model):
  

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    item = models.ForeignKey(MandiMenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(MandiMenuItem,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    comment=models.TextField(max_length=200)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self) -> str:
        return self.comment

