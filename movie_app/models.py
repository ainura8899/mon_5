from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    director = models.ForeignKey('Director', on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title

STARS = ((i, str(i)) for i in range(1, 6))


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=STARS, null=True, blank=True)

    def __str__(self):
        return self.movie.title
