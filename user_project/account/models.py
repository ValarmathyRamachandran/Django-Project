from django.db import models


# Create your models here.

class Account(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=20)
    new_password = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.id
