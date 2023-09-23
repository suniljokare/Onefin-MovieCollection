from .models import RequestCount

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Increment the request count
        request_count, _ = RequestCount.objects.get_or_create(id=1)
        request_count.count += 1
        request_count.save()

        response = self.get_response(request)
        return response




# class RequestCounterMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.request_count = 0

#     def __call__(self, request):
#         # Increment the request count for each incoming request
#         self.request_count += 1
#         response = self.get_response(request)
#         return response