from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExhibitionForm
import uuid
import boto3
from .models import Art, Exhibition, Theme, Photo

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'artcollector-sei'

class ArtCreate(LoginRequiredMixin, CreateView):
    model = Art
    fields = ['title', 'artist', 'created', 'description', 'media']
    success_url = '/art/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ArtUpdate(LoginRequiredMixin, UpdateView):
    model = Art
    fields = ['description', 'media']
    success_url = '/art/'

class ArtDelete(LoginRequiredMixin, DeleteView):
    model = Art
    success_url = '/art/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def art_index(request):
    art = Art.objects.filter(user=request.user)
    return render(request, 'art/index.html', {
        'art': art
    })

@login_required
def art_detail(request, art_id):
    art = Art.objects.get(id=art_id)
    theme_art_doesnt_have = Theme.objects.exclude(id__in = art.themes.all().values_list('id'))
    expo_form = ExhibitionForm()
    return render(request, 'art/detail.html', {
        'art': art,
        'expo_form': expo_form,
        'themes': theme_art_doesnt_have
    })

@login_required
def assoc_theme(request, art_id, theme_id):
    Art.objects.get(id=art_id).themes.add(theme_id)
    return redirect('detail', art_id=art_id)

@login_required
def unassoc_theme(request, art_id, theme_id):
    Art.objects.get(id=art_id).themes.remove(theme_id)
    return redirect('detail', art_id=art_id)

@login_required
def add_expo(request, art_id):
    form = ExhibitionForm(request.POST)
    if form.is_valid():
        new_expo = form.save(commit=False)
        new_expo.art_id = art_id
        new_expo.save()
    return redirect('detail', art_id=art_id)

@login_required
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

class ThemeList(LoginRequiredMixin, ListView):
    model = Theme

class ThemeDetail(LoginRequiredMixin, DetailView):
    model = Theme

class ThemeCreate(LoginRequiredMixin, CreateView):
    model = Theme
    fields = '__all__'
    success_url = '/themes/'

class ThemeUpdate(LoginRequiredMixin, UpdateView):
    model = Theme
    fields = '__all__'
    success_url = '/themes/'

class ThemeDelete(LoginRequiredMixin, DeleteView):
    model = Theme
    success_url = '/themes/'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)