from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('art/', views.art_index, name='index'),
    path('artwork/<int:art_id>', views.art_detail, name='detail'),
    path('artwork/create', views.ArtCreate.as_view(), name='art_create'),
]