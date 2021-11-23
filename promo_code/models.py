from django.db import models

# Create your models here.
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField(default=0.0)
    valid_from = models.DateField()
    valid_to = models.DateField()
    used = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.code