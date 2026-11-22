import time
from django.utils import timezone

class RequestTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        print(f"Request time: {duration:.4f} seconds")

        return response
# pyrefly: ignore[parse-error]
class UserStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_seen = timezone.now()
            request.user.save()
        response = self.get_response(request)
        return response