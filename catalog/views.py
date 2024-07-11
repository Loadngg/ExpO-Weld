from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import SearchForm
from .models import Category, Product, Brand


class CategoryListView(ListView):
    """Список категорий"""

    model = Category
    queryset = Category.objects.filter(parent_category=None).order_by('name')
    ordering = ['name']


class CategoryDetailView(DetailView):
    """Страница категории"""

    model = Category
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        descendants = self.get_descendants(category)
        descendants.insert(0, category)
        products = Product.objects.filter(parent_category__in=descendants)
        context["categories_list"] = Category.objects.filter(parent_category__slug=self.kwargs['slug'])
        context['products'] = products.order_by('name')
        return context

    def get_descendants(self, category):
        descendants = []
        for child in category.category_set.all():
            descendants.append(child)
            descendants.extend(self.get_descendants(child))
        return descendants


class ProductDetailView(DetailView):
    """Страница продукта"""

    model = Product
    slug_field = "slug"


class SearchView(View):
    """Страница результатов поиска"""

    @staticmethod
    def post(request):
        form = SearchForm(request.POST)

        if form.is_valid():
            search_field = form.cleaned_data.get('search_field')

            products_list = []
            products = Product.objects.filter(
                Q(parent_category_id__isnull=False) &
                (
                        Q(name__iregex=search_field) |
                        Q(article__iregex=search_field)
                )
            )

            for item in products:
                if item.parent_category is None:
                    continue

                products_list.append(item)

            queryset = {
                "search_field": search_field,
                "products": set(products_list)
            }
            return render(request, "catalog/search_results.html", queryset)
        return redirect("/")


class BrandListView(ListView):
    """Список брендов"""

    model = Brand
    queryset = Brand.objects.all().order_by('name')
    ordering = ['name']
