from django.db import models
from django.urls import reverse
from django.conf import settings


class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        blank=True, null=True, 
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
    text = models.TextField(default='')

    class Meta:
        unique_together = ['list', 'text']
