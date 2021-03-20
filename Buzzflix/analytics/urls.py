from django.urls import path


from .api import TrackingView, AnalyticsView

urlpatterns = [
    path('track/', TrackingView.as_view(), name="tracking"),
    path('analytics/', AnalyticsView.as_view(), name="analytics"),
    ]