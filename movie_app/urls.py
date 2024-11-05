from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('movies/', views.MovieListAPIView.as_view(), name='movie_list'),
    path('movies/<int:id>/', views.MovieDetailAPIView.as_view(), name='movie_detail'),

    path('directors/', views.DirectorListAPIView.as_view(), name='director_list'),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view(), name='director_detail'),

    path('reviews/', views.ReviewListAPIView.as_view(), name='review_list'),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view(), name='review_detail'),
]