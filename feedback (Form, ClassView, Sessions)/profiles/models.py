from django.db import models

# Create your models here.


class UserProfile(models.Model):
    image = models.ImageField(upload_to="images") # It would create image folder for you
