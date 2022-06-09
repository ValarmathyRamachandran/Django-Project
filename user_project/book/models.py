from django.db import models


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200, null=True)
    Author = models.CharField(max_length=200, null=True)
    Price = models.IntegerField()
    Edition = models.IntegerField()
    quantity = models.IntegerField(blank=False)
    image_field = models.FileField(upload)
    date_created
    rating = models.IntegerField
    date_updated
    description
    total_

    def __str__(self):
        return str(self.title)



