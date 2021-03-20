import datetime

from django.utils import timezone
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Tracking
from .utils import track_user_event
from .serializers import TrackingSerializer, TopReportSerializer

class TrackingView(generics.CreateAPIView):
    serializer_class = TrackingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Override to simplify response, instead of unnecessary full model data,
        which is unnecessary for clients
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({'result': True}, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnalyticsView(APIView):
    """Summary
    """
    
    def get(self, request):
        report = request.query_params.get('report')
        today = timezone.now()
        day = today - datetime.timedelta(days=7)
        if report == 'top_view':
            # what is the top viewed movie in the last 7 days (a view = a user watches a movie until the end)
            ts = Tracking.objects\
                .filter(
                    event_name='MOVIE_FINISH',
                    created_at__gte=day)\
                .values('movie', 'movie__title')\
                .annotate(count=Count('id'))\
                .order_by('-count')[:50]

            serializer = TopReportSerializer(ts, many=True)
            return Response(serializer.data)
        elif report == 'top_aband':
            # what is the most abandoned movie in the last 7 days (an abandonment = a user starts watching a movie, but has not yet reached the end of it)
            finished = Tracking.objects.filter(event_name='MOVIE_FINISH').values('movie').distinct()
            not_finished = Tracking.objects\
                .filter(
                    event_name='MOVIE_START',
                    created_at__gte=day)\
                .exclude(movie_id__in=finished)\
                .values('movie', 'movie__title')\
                .annotate(count=Count('id'))\
                .order_by('-count')[:50]

            serializer = TopReportSerializer(not_finished, many=True)
            return Response(serializer.data)
        else:
            pass

        return Response({})