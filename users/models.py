from django.db import models
from django.contrib.auth.models import User, AbstractUser
from orders.common import OrderStatus


class User(AbstractUser):
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def shipping_address(self):
        return self.shippingadresses_set.filter(is_default=True).first()

    def has_shipping_address(self):
        return self.shipping_address is not None

    def orders_completed(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')



# proxy model: to extend functionalities
class Customer(User):
    class Meta:
        proxy = True

    def get_products(self):
        return []


# one 2 one: to extend new attribs
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    lol = models.TextField()


# AbstractUser / AbstractBaseUser

