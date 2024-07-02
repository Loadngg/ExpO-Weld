from django.views.generic import TemplateView
from catalog.models import Product


class HomeView(TemplateView):
    template_name = "landing/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['popular_products'] = Product.objects.filter(is_popular=True)
        return context
