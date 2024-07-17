from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("services/demonstration", views.ServicesDemonstrationView.as_view(), name="services.demonstration"),
    path("services/delivery", views.ServicesDeliveryView.as_view(), name="services.delivery"),
    path("services/warranty", views.ServicesWarrantyView.as_view(), name="services.warranty"),
    path("services/repair", views.ServicesRepairView.as_view(), name="services.repair"),
    path("services/leasing", views.ServicesLeasingView.as_view(), name="services.leasing"),
]
