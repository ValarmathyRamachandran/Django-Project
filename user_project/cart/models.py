from django.contrib.auth.models import User
from django.db import models
from book.models import Book
from django.utils import timezone


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.FloatField()
    total_price = models.FloatField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.book_id)
