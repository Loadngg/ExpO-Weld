from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.conf import settings

from catalog.models import Product, Brand
from landing.forms import CallbackForm
from landing.models import PopularQuestion, YouTubeVideo


class HomeView(TemplateView):
    """Главная"""

    template_name = "landing/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['popular_products'] = Product.objects.filter(is_popular=True)
        context['popular_questions'] = PopularQuestion.objects.all()
        context['brands'] = Brand.objects.all()
        context['videos'] = YouTubeVideo.objects.all()
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


class CallbackView(View):
    """Форма обратного звонка"""

    @staticmethod
    def post(request):
        form = CallbackForm(request.POST)

        if not form.is_valid():
            error_message = "Проверьте введённые данные"
            return JsonResponse({'success': False, 'error_message': error_message})

        subject = form.cleaned_data.get("full_name")
        tel = form.cleaned_data.get("phone_number")
        message = form.cleaned_data.get("message")
        article = form.cleaned_data.get("article")
        send_mail(f"{subject} {tel} артикул: {article}", message, settings.EMAIL_HOST_USER, [settings.EMAIL_STORAGE])
        form.save()

        success_message = "Ваш запрос был удачно отправлен"
        return JsonResponse({'success': True, 'error_message': '', 'success_message': success_message})
