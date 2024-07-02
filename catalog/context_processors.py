from .models import Category


def categories(request):
    category_list = Category.objects.filter(parent_category=None)
    return {'context_categories': category_list.order_by('name')}
