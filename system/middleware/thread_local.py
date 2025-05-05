import threading

_thread_local = threading.local()

class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the authenticated user in thread-local storage
        if request.user.is_authenticated:
            _thread_local.user = request.user
        else:
            _thread_local.user = None
        # print('thread_local user : ', _thread_local.user)
        # print('thread_local user id : ', _thread_local.user.id)
        response = self.get_response(request)
        return response