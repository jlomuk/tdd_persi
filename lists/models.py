from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
    text = models.TextField()