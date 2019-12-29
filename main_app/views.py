from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Art

class ArtCreate(CreateView):
    model = Art
    fields = '__all__'
    success_url = '/art/'

class ArtUpdate(UpdateView):
    model = Art
    fields = ['description', 'media']
    success_url = '/art/'

class ArtDelete(DeleteView):
    model = Art
    success_url = '/art/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def art_index(request):
    artwork = Art.objects.all()
    return render(request, 'art/index.html', {
        'artwork': artwork
    })

def art_detail(request, art_id):
    artwork = Art.objects.get(id=art_id)
    return render(request, 'art/detail.html', {
        'artwork': artwork
    })