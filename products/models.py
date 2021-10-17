import uuid
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.
class Product(models.Model):
    """Product"""
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0) #123456.50
    image = models.ImageField(upload_to='products/', null=False, blank=False)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """changes the title"""
        return str(self.title)


def create_slug(sender, instance, *args, **kwargs): #callback
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        while Product.objects.filter(slug=slug).exists():
            slug = slugify(f"{instance.title}-{str(uuid.uuid4())[:8]}")
        instance.slug = slug


pre_save.connect(create_slug, sender=Product)