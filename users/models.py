from django.db import models
from django.contrib.auth.models import User, AbstractUser



class User(AbstractUser):
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


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

