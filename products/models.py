from django.db import models

# Create your models here.
class Product(models.Model):
    """Product"""
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0) #123456.50
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        "changes the title"
        return str(self.title)
