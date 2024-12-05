from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your book models here.

class Book(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    author = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(blank=False)
    quantity = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    description = models.TextField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image_field = models.ImageField(upload_to='static/', max_length=200, null=True, default=None)
    rating = models.IntegerField(null=True, blank=True)
    total_book_added = models.IntegerField(default=1, blank=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
