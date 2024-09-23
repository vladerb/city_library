from django.http import HttpRequest

from archive.models import Category


def categories_processor(request: HttpRequest):
    categories = Category.objects.order_by('title')
    return {'categories': categories}