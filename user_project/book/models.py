from django.db import models


# Create your book models here.

class Book(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    author = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False)
    description = models.TextField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # image_field = models.FileField(upload_to='', max_length=200, null=True, default=None)

    # rating = models.IntegerField()
    # total_book_added = models.IntegerField()

    #

    # date_updated = models.DateTimeField()

    def __str__(self):
        return str(self.name)
