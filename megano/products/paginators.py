"""
Paginators for products app views.
"""
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CatalogPaginator(PageNumberPagination):
    """
    Paginator for catalog views.

    Attributes:
        page_size: Default page size.
        page_size_query_param: Which query param used as page size.
        page_query_param: Which query param used as current page number.
        max_page_size: Max page size.

    Methods:
        get_paginated_response:
            Get response with paginated data.
            (Redefined to correctly returns data to frontend)
    """
    page_size = 30
    page_size_query_param = 'limit'
    page_query_param = 'currentPage'
    max_page_size = 100

    def get_paginated_response(self, data: list):
        """
        Get response with paginated data.

        Returns:
            Response: response with data.
        """
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages,
        })