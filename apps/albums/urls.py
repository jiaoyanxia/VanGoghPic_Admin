from django.urls import path

from apps.albums.views import AlbumsView, AlbumData, SignAlbumView, createAlbums, getFavorites, reFavorites, \
    isFavorites, myFavorites, testFavorites, updataAlbum

urlpatterns = [
    path('album/', SignAlbumView.as_view()),
    path('albums/', AlbumData.as_view()),
    path('createAlbum/', createAlbums.as_view()),
    path('getFavorites/', getFavorites.as_view()),
    path('reFavorites/', reFavorites.as_view()),
    path('isFavorites/', isFavorites.as_view()),
    path('myFavorites/', myFavorites.as_view()),
    path('testFavorites/<user>/', testFavorites.as_view()),
    path('updataAlbum/', updataAlbum.as_view()),
]
