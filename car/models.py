from django.db import models
from brand.models import Brand
from django.contrib.auth.models import User

# Create your models here.
class Car(models.Model):
    car_name = models.CharField(max_length=100)
    car_price = models.DecimalField(max_digits=10, decimal_places=2)
    car_view_details = models.TextField()
    quantity = models.IntegerField(default=1)
    car_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='car')
    image = models.ImageField(upload_to='car/media/uploads/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.car_name 
    

class Comment(models.Model):
    post = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) # jkhn e ei class er object toiri hobe sei time ta rekhe dibe
    
    def __str__(self):
        return f"Comments by {self.name}"