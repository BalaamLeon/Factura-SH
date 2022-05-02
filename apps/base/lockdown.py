import re
from django.conf import settings
from django.contrib.auth.decorators import login_required

# for registering a class as middleware you at least __init__() and __call__() for this case we additionally need
# process_view() which will be automatically called by Django before rendering a view / template


LOGIN_REQUIRED_URLS = [
    re.compile(url) for url in getattr(settings, "LOGIN_REQUIRED_URLS", [])
]

LOGIN_REQUIRED_URLS_EXCEPTIONS = [
    re.compile(url) for url in getattr(settings, "LOGIN_REQUIRED_URLS_EXCEPTIONS", [])
]


class LoginRequiredMiddleware(object):
    # need for one time initialization, here response is a function which will be called to get response from view /
    # template

    def __init__(self, response):
        self.get_response = response
        # self.required = tuple(re.compile(url) for url in settings.AUTH_URLS)
        # self.exceptions = tuple(re.compile(url) for url in settings.NO_AUTH_URLS)

    def __call__(self, request):
        # any code here will be called before requesting response
        response = self.get_response(request)
        # any code written here will be called after response
        return response

    # this is called before requesting response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated:
            return None

        # An exception match should immediately return None
        for url in LOGIN_REQUIRED_URLS_EXCEPTIONS:
            if url.match(request.path):
                return None

        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in LOGIN_REQUIRED_URLS:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)

        # Explicitly return None for all non-matching requests
        return None