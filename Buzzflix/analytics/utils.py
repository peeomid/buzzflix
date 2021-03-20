from .models import Tracking

def track_user_event(event_name, request, movie_id, metadata):
    """Track User event
    
    Args:
        event_name (TYPE): Description
        request (TYPE): Description
        movie_id (TYPE): Description
        metadata (TYPE): Description
    """
    return Tracking.objects.create(
            event_name=event_name,
            user=request.user,
            movie_id=movie_id,
            metadata=metadata
        )
