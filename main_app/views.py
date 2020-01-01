from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import ExhibitionForm
from .models import Art, Exhibition, Theme
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'artcollector-sei'

class ArtCreate(CreateView):
    model = Art
    fields = ['title', 'artist', 'created', 'description', 'media']
    success_url = '/art/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
    art = Art.objects.all()
    return render(request, 'art/index.html', {
        'art': art
    })

def art_detail(request, art_id):
    art = Art.objects.get(id=art_id)
    theme_art_doesnt_have = Theme.objects.exclude(id__in = art.themes.all().values_list('id'))
    expo_form = ExhibitionForm()
    return render(request, 'art/detail.html', {
        'art': art,
        'expo_form': expo_form,
        'themes': theme_art_doesnt_have
    })

def assoc_theme(request, art_id, theme_id):
    Art.objects.get(id=art_id).themes.add(theme_id)
    return redirect('detail', art_id=art_id)

def unassoc_theme(request, art_id, theme_id):
    Art.objects.get(id=art_id).themes.remove(theme_id)
    return redirect('detail', art_id=art_id)

def add_expo(request, art_id):
    form = ExhibitionForm(request.POST)
    if form.is_valid():
        new_expo = form.save(commit=False)
        new_expo.art_id = art_id
        new_expo.save()
    return redirect('detail', art_id=art_id)

class ThemeList(ListView):
    model = Theme

class ThemeDetail(DetailView):
    model = Theme

class ThemeCreate(CreateView):
    model = Theme
    fields = '__all__'
    success_url = '/themes/'

class ThemeUpdate(UpdateView):
    model = Theme
    fields = '__all__'
    success_url = '/themes/'

class ThemeDelete(DeleteView):
    model = Theme
    success_url = '/themes/'

def add_photo(request, art_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try: 
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print('url:', url)
            photo = Photo(url=url, art_id=art_id)
            photo.save()
            print(photo, 'photo saved')
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', art_id=art_id)