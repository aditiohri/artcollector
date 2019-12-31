from django.db import models
from django.urls import reverse

TYPES_OF_EXHIBITIONS = (
    ('S', 'Solo'),
    ('D', 'Duo'),
    ('G', 'Group'),
    ('P', 'Permanent'),
)

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

class Exhibition(models.Model):
    start_date = models.DateField('Beginning of Exhibition')
    end_date = models.DateField('End Date - Optional', blank=True, null=True)
    venue = models.TextField(max_length=150)
    show = models.CharField(
        max_length=1,
        choices=TYPES_OF_EXHIBITIONS,
        default=TYPES_OF_EXHIBITIONS[0][0]
        )
    art = models.ForeignKey(Art, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_show_display()} starting {self.start_date}'