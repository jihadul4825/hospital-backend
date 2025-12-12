from rest_framework.pagination import PageNumberPagination

class DoctorPagination(PageNumberPagination):
    page_size = 1 # item per page
    page_size_query_param = 'page_size'
    max_page_size = 100