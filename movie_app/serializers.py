from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ['id', 'name', 'movie_count']

    def get_movie_count(self, director):
        return director.movies.count()

class DirectortValiditySerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'movie', 'stars']

class ReviewValiditySerializer(serializers.Serializer):
    text = serializers.CharField(min_length=2, max_length=100)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    def validate_text(self, value):
        if 'bad' in value:
            raise serializers.ValidationError('Bad text is not allowed')
        return value

class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True, required=False)
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'director', 'duration', 'reviews', 'average_rate']

    def get_average_rate(self, movies):
        reviews = movies.reviews.all()
        if reviews:
            sum_reviews = sum([i.stars for i in reviews])
            average = sum_reviews / len(reviews)
            return average
        return None

    def create(self, validated_data):
        # Extract director data
        director_data = validated_data.pop('director')

        # Either get an existing director or create a new one
        director, created = Director.objects.get_or_create(**director_data)

        # Create the movie without the reviews field, which is read-only
        movie = Movie.objects.create(director=director, **validated_data)

        return movie

class MovieValiditySerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    description = serializers.CharField(min_length=10)
    duration = serializers.IntegerField(min_value=1)
    director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all())