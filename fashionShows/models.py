from django.db import models


class Article(models.Model):
    text = models.TextField()
    image_url = models.CharField(max_length=500)
