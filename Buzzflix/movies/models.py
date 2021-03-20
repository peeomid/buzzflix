from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.TextField(blank=False, unique=True)
    synopsis = models.TextField()
    poster_image = models.URLField()
    is_highlighted = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', through='MovieCategory', related_name='movies')
    display_on_home = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=128, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class MovieCategory(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)