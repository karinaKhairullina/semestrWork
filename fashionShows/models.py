from django.db import models
from authorization.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.url

class ClothingItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fashion_show_items')

    def __str__(self):
        return self.name

class Outfit(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    clothing_items = models.ManyToManyField(ClothingItem)

    def __str__(self):
        return self.name

class FashionShow(models.Model):
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.location} {self.date} {self.time}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fashion_show = models.ForeignKey(FashionShow, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} subscribed to {self.fashion_show}"

class FavoriteOutfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.outfit}"