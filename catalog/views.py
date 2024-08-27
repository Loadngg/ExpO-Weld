from django.db.models import Q, F, Func, Value
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import SearchForm
from .models import Category, Product, Brand, ProductSpecType, ProductFilterValue


class CategoryListView(ListView):
    """Список категорий"""

    model = Category
    queryset = Category.objects.filter(parent_category=None).order_by('name')
    ordering = ['name']


def get_spec_types_filters(products, category):
    spec_types = {}
    brands = {}

    for product in products:
        for spec in product.productspec_set.all():
            if not spec.type.is_filter:
                continue

            if spec.type.categories is None:
                continue

            ancestors = category.get_ancestors()
            ancestors.append(category)

            descendants = category.get_descendants()
            descendants.append(category)

            if not any(ancestor in spec.type.categories.all() for ancestor in list(set(ancestors + descendants))):
                continue

            spec_filter_values = ProductFilterValue.objects.filter(filter=spec.type)
            if len(spec_filter_values) == 0:
                continue

            if spec.type not in spec_types:
                spec_types[spec.type] = []

            spec_values = []
            for value in spec_filter_values:
                spec_values.append(value.value.replace(",", "."))

            spec_types[spec.type] = spec_values

        if not product.brand:
            continue

        if product.brand.name not in brands:
            brands[product.brand.name] = []
        brands[product.brand.name].append(product.brand.name)

    sorted_spec_types = {}

    for key in sorted(spec_types.keys(), key=lambda x: x.position):
        values = sorted(list(set(spec_types[key])))
        if len(values) == 1:
            continue

        sorted_spec_types[key] = values

    sorted_brands = sorted(brands.keys())

    return sorted_spec_types, sorted_brands


class CategoryDetailView(DetailView):
    """Страница категории"""

    model = Category
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context["categories_list"] = Category.objects.filter(parent_category__slug=self.kwargs['slug'])
        spec_types, brands = get_spec_types_filters(category.product_set.all(), category)
        context["spec_types"] = spec_types
        context["brands"] = brands

        products = category.products
        selected_specs = self.request.GET

        if len(selected_specs) == 0:
            context['products'] = products
            return context

        products_list = []
        spec_type_ids = []
        spec_type_values = []
        selected_brands = []

        has_specs = False
        for spec_str in selected_specs:
            if not spec_str.startswith('spec_'):
                continue

            has_specs = True

        if not has_specs:
            products_list = products

        for spec_str in selected_specs:
            if not spec_str.startswith('spec_'):
                continue

            spec = spec_str.replace('spec_type_id_', '').split("_spec_")
            spec_type_id = int(spec[0])
            spec_type_ids.append(spec_type_id)

            spec_value = spec[1]
            spec_type_values.append(spec_value)
            spec_type = ProductSpecType.objects.get(id=spec_type_id)

            products_list += Product.objects.annotate(
                replaced_value=Func(F('productspec__value'), Value(','), Value('.'), function='REPLACE')
            ).filter(
                Q(replaced_value__iregex=spec_value) & Q(productspec__type=spec_type) & Q(parent_category__slug=self.kwargs['slug'])
            )

        for spec_str in selected_specs:
            if not spec_str.startswith('brand_'):
                continue

            brand_name = spec_str.replace('brand_', '')
            selected_brands.append(brand_name)

        if len(selected_brands) != 0:
            products_list = [product for product in products_list if product.brand.name in selected_brands]

        context['spec_type_ids'] = spec_type_ids
        context['spec_type_values'] = spec_type_values
        context['selected_brands'] = selected_brands
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
