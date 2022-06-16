from book.models import Book
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)],null=False)
    address = models.TextField(max_length=300, null=False)
    total_price = models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.name
