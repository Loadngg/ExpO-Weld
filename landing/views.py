from django.views.generic import TemplateView
from catalog.models import Product, Brand


class HomeView(TemplateView):
    """Главная"""

    template_name = "landing/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['popular_products'] = Product.objects.filter(is_popular=True)
        context['brands'] = Brand.objects.all()
        return context


class ContactsView(TemplateView):
    """Контакты"""

    template_name = "landing/contacts.html"


class AboutView(TemplateView):
    """О нас"""

    template_name = "landing/about.html"


class ServicesView(TemplateView):
    """Услуги"""

    template_name = "landing/services.html"


class ServicesDemonstrationView(TemplateView):
    """Услуги/Демонстрация"""

    template_name = "landing/services_demonstration.html"


class ServicesDeliveryView(TemplateView):
    """Услуги/Доставка"""

    template_name = "landing/services_delivery.html"


class ServicesWarrantyView(TemplateView):
    """Услуги/Гарантия"""

    template_name = "landing/services_warranty.html"


class ServicesRepairView(TemplateView):
    """Услуги/Ремонт"""

    template_name = "landing/services_repair.html"


class ServicesLeasingView(TemplateView):
    """Услуги/Лизинг"""

    template_name = "landing/services_leasing.html"
