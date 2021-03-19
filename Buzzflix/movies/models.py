from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.TextField()
    synopsis = models.TextField()
    poster_image = models.URLField()
    is_highlighted = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, through="MovieCategory")

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class MovieCategory(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)