from django.db import models
from django.contrib.auth.models import User
 

# Create your models here.


from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
