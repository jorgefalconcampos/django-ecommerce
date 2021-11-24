import string
import random

from django.db import models
from django.db.models.signals import pre_save

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

def set_code(sender, instance, *args, **kwargs):
    if instance.code:
        return

    chars = string.ascii_uppercase + string.digits
    instance.code = ''.join(random.choice(chars) for _ in range(random.randint(6, 10)) )


#before an object of type PromoCode, executes the save method, will execute the set_code method
pre_save.connect(set_code, sender=PromoCode) 