from django.contrib import admin
from .models import Art, Exhibition, Theme, Photo

admin.site.register(Art)
admin.site.register(Exhibition)
admin.site.register(Theme)
admin.site.register(Photo)