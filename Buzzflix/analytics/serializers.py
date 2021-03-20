from rest_framework import serializers

from .models import Tracking

class TrackingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Tracking
        fields = ('event_name', 'user', 'movie', 'value', 'metadata')

class TopReportSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='movie')
    title = serializers.CharField(source='movie__title')
    count = serializers.IntegerField()