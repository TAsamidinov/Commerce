from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    watchlist = models.ManyToManyField('Listing', related_name='watchers', blank=True)

    def __str__(self):
        return f"{self.id}. {self.username}: {self.name} {self.surname} {self.email}"

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
  
    def __str__(self):
        return f"{self.id} {self.title} {self.price}  ({self.owner.username})"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.listing.title} {self.user.username} {self.content[:20]}..."

class Bid(models.Model):
    listing = models.ForeignKey(Listing, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.listing.title} {self.user.username} {self.amount}"

