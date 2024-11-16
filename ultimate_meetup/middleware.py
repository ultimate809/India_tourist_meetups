from django.http import HttpResponseRedirect
from django.urls import reverse
import os

class URLRewriteMiddleware:
    """
    Middleware to rewrite URLs by removing the '/dev/' part from the request URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with /dev/ and rewrite it
        if request.path.startswith('/dev/'):
            os.environ['ENVIRONMENT'] = 'dev'
        elif request.path.startswith('/prod/'):
            os.environ['ENVIRONMENT'] = 'prod'
        elif request.path.startswith('/test/'):
            os.environ['ENVIRONMENT'] = 'test'
        else:
            os.environ['ENVIRONMENT'] = 'test'
            # request.path = 'test/' + request.path

        print(os.getenv('ENVIRONMENT'))

        # Continue processing the request if no rewriting is needed
        response = self.get_response(request)
        return response
