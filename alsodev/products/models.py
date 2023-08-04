from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Feature(models.Model):
    value = models.CharField(max_length=100)
    key = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.key}:{self.value}'


class Image(models.Model):
    image = models.ImageField(upload_to='')


class Product(models.Model):
    slug = models.SlugField(max_length=200, default='')

    author = models.ForeignKey(
        User,
        related_name='products',
        on_delete=models.CASCADE
    )

    price = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    feature = models.ManyToManyField(
        Feature,
        related_name='product'
    )

    images = models.ManyToManyField(
        Image,
        related_name='images'
    )

    def __str__(self):
        return self.slug

