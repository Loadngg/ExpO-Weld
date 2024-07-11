from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand_site", "get_image")
    list_display_links = ("id", "name")
    readonly_fields = ("get_image",)
    search_fields = ("name",)

    fieldsets = (
        ("Основная информация", {"fields": ("name", "description", "brand_site")}),
        ("Логотип", {"fields": (("logo", "get_image"),)})
    )

    def get_image(self, obj):
        if obj.logo:
            return mark_safe(f'<img src={obj.logo.url} width="100" height="110">')

        return mark_safe(f'<img src="https://place-hold.it/100" width="100" height="100">')

    get_image.short_description = "Логотип бренда"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_image")
    list_display_links = ("id", "name")
    list_filter = ["parent_category"]
    save_as = True
    readonly_fields = ("get_image", "slug")
    search_fields = ("name",)
    autocomplete_fields = ("parent_category",)

    fieldsets = (
        ("Основная информация", {"fields": ("name", ("image", "get_image"),)}),
        ("Родительская категория", {"fields": ("parent_category",)}),
        ("Опции", {"fields": (("slug",),)}),
    )

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100" height="110">')
        else:
            return mark_safe(f'<img src="https://place-hold.it/100" width="100" height="100">')

    get_image.short_description = "Изображение"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "article", "price", "parent_category", "is_popular")
    list_display_links = ("id", "name")
    list_editable = ("is_popular",)
    readonly_fields = ("slug",)
    autocomplete_fields = ("brand", "parent_category")
    search_fields = ("name", "article")
    list_filter = ["parent_category"]
    inlines = [ProductImageInline]

    fieldsets = (
        ("Основная информация", {"fields": ("name", "description", ("article", "price"))}),
        ("Принадлежность", {"fields": ("brand", "parent_category",)}),
        ("Опции", {"fields": ("is_popular", "slug")})
    )
    save_as = True
