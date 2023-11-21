from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass



class Category(models.Model):
    category_name = models.CharField(max_length=50)  
    def __str__(self):
        return f"{self.category_name}"
    
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}" 
   
class Bid(models.Model):
    bid=models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")

    def __str__(self):
        return f"{self.bid}" 

class Listing(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    imageurl = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_price")
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watch_list")

    def __str__(self):
        return f"{self.title}"


    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="authorname")
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingname")
    message= models.CharField(max_length=300)
    
    def __str__(self) -> str:
        return f'{self.author} commented on {self.listing}'
    
    
    
    
    
    
    
    
    