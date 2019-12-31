from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('art/', views.art_index, name='index'),
    path('art/<int:art_id>', views.art_detail, name='detail'),
    path('art/create', views.ArtCreate.as_view(), name='art_create'),
    path('art/<int:pk>/update', views.ArtUpdate.as_view(), name='art_update'),
    path('art/<int:pk>/delete', views.ArtDelete.as_view(), name='art_delete'),
    path('art/<int:art_id>/add_expo', views.add_expo, name='add_expo'),
]