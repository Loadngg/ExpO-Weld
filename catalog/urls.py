from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    path('r"^search_results/$"', views.SearchView.as_view(), name='search')
]
