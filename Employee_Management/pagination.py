# DialUrbanPropVichaarBackend/pagination.py
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import math
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = 'page_size'  # Allow user to set page size
    max_page_size = 100  # Prevent large queries

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_count': self.page.paginator.count,
            'total_pages': math.ceil(self.page.paginator.count / self.page_size) if self.page_size else 0,
            'data': data
        })
        
    def get_previous_link(self):
        if not self.page.has_previous():
            return None

        request_url = self.request.build_absolute_uri()
        previous_page_number = self.page.previous_page_number()

        # Parse the URL and modify the query params
        url_parts = urlparse(request_url)
        query_params = parse_qs(url_parts.query)
        query_params[self.page_query_param] = [str(previous_page_number)]  # Set previous page number

        # Build the new URL
        new_query_string = urlencode(query_params, doseq=True)
        new_url = urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path, url_parts.params, new_query_string, url_parts.fragment))

        return new_url