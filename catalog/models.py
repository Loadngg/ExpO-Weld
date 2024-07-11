from django.db import models
from django.urls import reverse

from modules.services.utils import unique_slugify


class Brand(models.Model):
    """Бренд"""

    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    brand_site = models.URLField("Сайт бренда", max_length=250, blank=True, null=True)
    logo = models.ImageField("Логотип", upload_to='brands/', blank=True, null=True)
    slug = models.SlugField(verbose_name="Ссылка", max_length=150, unique=True, default='', editable=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = unique_slugify(self, value)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Category(models.Model):
    """Категория"""

    name = models.CharField("Название", max_length=150)
    image = models.ImageField("Изображение", upload_to='category/', blank=True, null=True)
    slug = models.SlugField(verbose_name="Ссылка", max_length=150, unique=True, default='', editable=False)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                        verbose_name="Родительская категория")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = unique_slugify(self, value)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """Товар"""

    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    article = models.CharField("Артикул", unique=True, max_length=100, default=0)
    price = models.DecimalField("Цена", default=0, decimal_places=2, max_digits=11)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    parent_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,
                                        verbose_name="Родительская категория")
    is_popular = models.BooleanField("Популярный товар", default=False)
    slug = models.SlugField(verbose_name="Ссылка", max_length=150, unique=True, default='', editable=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = unique_slugify(self, value)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    @property
    def first_image(self):
        image = None

        if len(self.productimage_set.all()) != 0:
            image = self.productimage_set.first()

        return image

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    """Фото товара"""

    image = models.ImageField("Изображение", upload_to='product/', blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    def __str__(self):
        return f"Изображение для товара '{self.product.name}'"

    class Meta:
        verbose_name = "Фотография товара"
        verbose_name_plural = "Фотографии товаров"
