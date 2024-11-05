from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectortValiditySerializer, ReviewValiditySerializer
from rest_framework.permissions import IsAuthenticated

class DirectorListAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def post(self, request, *args, **kwargs):
        validator = DirectortValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': validator.errors})
        name = validator.validated_data['name']
        Director.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED)

class DirectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        name_detail = self.get_object()
        validator = DirectortValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': validator.errors})
        name_detail.name = validator.validated_data['name']
        name_detail.save()
        return Response(status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class MovieListAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        print(request.user)
        validator = MovieSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': validator.errors})
        title = validator.validated_data['title']
        description = validator.validated_data['description']
        duration = validator.validated_data['duration']
        director_data = validator.validated_data['director']
        director, created = Director.objects.get_or_create(**director_data)
        Movie.objects.create(title=title, description=description, duration=duration, director=director)
        return Response(status=status.HTTP_201_CREATED)


class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        movie_detail = self.get_object()
        validator = MovieSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': validator.errors})
        movie_detail.title = validator.validated_data['title']
        movie_detail.description = validator.validated_data['description']
        movie_detail.duration = validator.validated_data['duration']
        director_data = validator.validated_data['director']
        director, created = Director.objects.get_or_create(**director_data)
        movie_detail.director = director
        movie_detail.save()
        return Response(status=status.HTTP_200_OK)

class ReviewListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        validator = ReviewValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': validator.errors})
        text = validator.validated_data['text']
        stars = validator.validated_data['stars']
        movie_id = validator.validated_data['movie'].id
        Review.objects.create(text=text, stars=stars, movie_id=movie_id)
        return Response(status=status.HTTP_201_CREATED)

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        review_detail = self.get_object()
        validator = ReviewValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': validator.errors})
        review_detail.text = validator.validated_data['text']
        review_detail.stars = validator.validated_data['stars']
        review_detail.save()
        return Response(status=status.HTTP_200_OK)

