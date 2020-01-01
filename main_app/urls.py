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
    path('art/<int:art_id>/add_expo', views.add_photo, name='add_photo'),
    path('art/<int:art_id>/add_photo', views.add_expo, name='add_expo'),
    path('art/<int:art_id>/assoc_theme/<int:theme_id>/', views.assoc_theme, name='assoc_theme'),
    path('art/<int:art_id>/unassoc_theme/<int:theme_id>/', views.unassoc_theme, name='unassoc_theme'),
    path('themes/', views.ThemeList.as_view(), name='theme_index'),
    path('themes/<int:pk>', views.ThemeDetail.as_view(), name='theme_detail'),
    path('themes/create/', views.ThemeCreate.as_view(), name='theme_create'),
    path('themes/<int:pk>/update/', views.ThemeUpdate.as_view(), name='theme_update'),
    path('themes/<int:pk>/delete/', views.ThemeDelete.as_view(), name='theme_delete'),
]