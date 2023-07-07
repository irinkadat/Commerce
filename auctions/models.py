from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.categoryName


class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, related_name="userBid") 



class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=300)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidp")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True,related_name="user" )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,related_name="category" )
    watchlist = models.ManyToManyField(User,blank=True,null=True,related_name="watchlistt"  )

    def __str__(self) -> str:
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='commentedlisting')
    message = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.author} comment on {self.listing}"
    
