from django.db import models

from users.models import User

# Create your models here.
class ShippingAdresses(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    reference = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.zip_code

    def update_default(self, default=False):
        self.is_default = default
        self.save()

    @property    
    def address(self):
        return f"{self.city} - {self.state} - {self.country}"

    
