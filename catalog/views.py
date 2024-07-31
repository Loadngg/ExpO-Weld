from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import SearchForm
from .models import Category, Product, Brand, ProductSpecType


class CategoryListView(ListView):
    """Список категорий"""

    model = Category
    queryset = Category.objects.filter(parent_category=None).order_by('name')
    ordering = ['name']


def get_spec_types_filters(products, category):
    spec_types = {}
    for product in products:
        for spec in product.productspec_set.all():
            if (
                    category not in spec.type.categories.all()
                    or spec.type.categories is None
                    or not spec.type.is_filter
            ):
                continue

            if spec.type not in spec_types:
                spec_types[spec.type] = []
            spec_types[spec.type].append(spec.value.replace(",", "."))

    sorted_spec_types = {}
    for key in sorted(spec_types.keys(), key=lambda x: x.name):
        values = sorted(list(set(spec_types[key])))
        if len(values) == 1:
            continue

        sorted_spec_types[key] = values

    return sorted_spec_types


class CategoryDetailView(DetailView):
    """Страница категории"""

    model = Category
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context["categories_list"] = Category.objects.filter(parent_category__slug=self.kwargs['slug'])
        context["spec_types"] = get_spec_types_filters(category.product_set.all(), category)

        products = category.products
        selected_specs = self.request.GET

        if len(selected_specs) == 0:
            context['products'] = products
            return context

        products_list = []
        spec_type_ids = []
        spec_type_values = []
        for spec_str in selected_specs:
            if spec_str.startswith('spec_'):
                spec = spec_str.replace('spec_type_id_', '').split("_spec_")
                spec_type_id = int(spec[0])
                spec_type_ids.append(spec_type_id)

                spec_value = spec[1]
                spec_type_values.append(spec_value)
                spec_type = ProductSpecType.objects.get(id=spec_type_id)

                products_list += products.filter(Q(productspec__value=spec_value) & Q(productspec__type=spec_type))

        context['spec_type_ids'] = spec_type_ids
        context['spec_type_values'] = spec_type_values
        context['products'] = set(products_list)
        return context


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


class BrandDetailView(DetailView):
    """Страница бренда"""

    model = Brand
    slug_field = "slug"
