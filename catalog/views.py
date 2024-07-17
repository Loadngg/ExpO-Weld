from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import SearchForm
from .models import Category, Product, Brand, ProductSpecType, ProductSpec


class CategoryListView(ListView):
    """Список категорий"""

    model = Category
    queryset = Category.objects.filter(parent_category=None).order_by('name')
    ordering = ['name']


def get_spec_types_filters():
    spec_types = {}
    spec_types_list = ProductSpecType.objects.all()
    for spec_type in spec_types_list:
        spec_types[spec_type] = list(
            set(ProductSpec.objects.filter(type__name=spec_type).values_list('value', flat=True).order_by("type__name")))

    return spec_types


class CategoryDetailView(DetailView):
    """Страница категории"""

    model = Category
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        descendants = self.get_descendants(category)
        descendants.insert(0, category)
        context["categories_list"] = Category.objects.filter(parent_category__slug=self.kwargs['slug'])
        context["spec_types"] = get_spec_types_filters()

        products = Product.objects.filter(parent_category__in=descendants)
        selected_specs = self.request.GET

        if len(selected_specs) == 0:
            context['products'] = products
            return context

        products_list = []
        spec_type_ids = []
        spec_type_values = []
        for spec_str in selected_specs:
            if spec_str.startswith('spec_'):
                spec = spec_str.replace('spec_type_id_', '')
                spec_type_id = int(spec[0])
                spec_type_ids.append(spec_type_id)

                spec_value = spec.split("_spec_")[1]
                spec_type_values.append(spec_value)
                spec_type = ProductSpecType.objects.get(id=spec_type_id)

                products_list += products.filter(Q(productspec__value=spec_value) & Q(productspec__type=spec_type))

        context['spec_type_ids'] = spec_type_ids
        context['spec_type_values'] = spec_type_values
        context['products'] = set(products_list)
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
