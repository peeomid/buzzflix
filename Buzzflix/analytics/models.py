from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from Buzzflix.movies.models import Movie

User = get_user_model()

# Create your models here.
class Tracking(models.Model):
    event_name = models.CharField(max_length=128, blank=False, db_index=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=True, on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)
    metadata = models.JSONField(null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.event_name} at {self.created_at}"