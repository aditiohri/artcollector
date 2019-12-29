from django.db import models
from django.urls import reverse

class Art(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    created = models.TextField(max_length=4)
    description = models.TextField(max_length=500)
    media = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'art_id': self.id})