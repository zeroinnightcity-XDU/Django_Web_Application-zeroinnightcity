from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("music/", views.music_list, name="music-list"),
    path("music/<int:pk>/", views.music_detail, name="music-detail"),
    path("film/", views.film_list, name="film-list"),
    path("film/<int:pk>/", views.film_detail, name="film-detail"),
    path("fragments/", views.fragments_list, name="fragments-list"),
    path("fragments/<int:pk>/", views.fragments_detail, name="fragments-detail"),
    path("thoughts/", views.thoughts_list, name="thoughts-list"),
    path("thoughts/<int:pk>/", views.thoughts_detail, name="thoughts-detail"),
    path("about/", views.about_view, name="about"),
]
