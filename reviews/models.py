import os
from PIL import Image

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Ticket(models.Model):
    IMAGE_MAX_SIZE = (700, 200)

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    # Save images with a maximum size
    def resize_image(self):
        if self.image:
            with Image.open(self.image) as image:
                image.thumbnail(self.IMAGE_MAX_SIZE)
                image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def delete(self, *args, **kwargs):
        if self.image:
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ZERO = 0, '☆☆☆☆☆'
        ONE = 1, '★☆☆☆☆'
        TWO = 2, '★★☆☆☆'
        THREE = 3, '★★★☆☆'
        FOUR = 4, '★★★★☆'
        FIVE = 5, '★★★★★'

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=Rating.choices,
        default=Rating.ZERO)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
