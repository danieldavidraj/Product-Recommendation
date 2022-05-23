from django.db import models

class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.TextField()
    product_id = models.TextField()
    ratings = models.TextField()
    timestamp = models.TextField()
