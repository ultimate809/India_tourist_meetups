import os
from django.http import HttpResponseRedirect
from urllib.parse import urlparse, urlunparse

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
        elif request.path.startswith('/stage/'):
            os.environ['ENVIRONMENT'] = 'stage'
        elif request.path.startswith('/test/'):
            os.environ['ENVIRONMENT'] = 'test'
        else:
            os.environ['ENVIRONMENT'] = 'test'
            # request.path = 'test/' + request.path

        # path = request.path
        print(request.path)
        print(os.getenv('ENVIRONMENT'))
        # if not request.path.endswith("/") and not request.path.endswith("."):
        #     # Parse the current URL
        #     parsed_url = urlparse(request.build_absolute_uri())
        #     # Add a trailing slash to the path
        #     new_path = f"{parsed_url.path}/"
        #     # Build the new URL
        #     new_url = urlunparse(parsed_url._replace(path=new_path))
        #     # Redirect to the new URL
        #     return HttpResponseRedirect(new_url)


        # Continue processing the request if no rewriting is needed
        response = self.get_response(request)
        return response
