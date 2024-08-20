from django.db import models
from django.urls import reverse

from modules.services.utils import unique_slugify
from tinymce.models import HTMLField


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
    position = models.PositiveIntegerField("Позиция в навигации", default=1, null=False, blank=False)
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

    def get_descendants(self):
        descendants = []
        for child in self.category_set.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def get_ancestors(self):
        ancestors = []
        current = self
        while current.parent_category is not None:
            ancestors.append(current.parent_category)
            current = current.parent_category
        return ancestors

    @property
    def products(self):
        descendants = self.get_descendants()
        descendants.insert(0, self)
        return Product.objects.filter(parent_category__in=descendants)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """Товар"""

    name = models.CharField("Название", max_length=150)
    short_description = models.TextField("Краткое описание")
    article = models.CharField("Артикул", unique=True, max_length=100, default=0)
    price = models.DecimalField("Цена", default=0, decimal_places=2, max_digits=11)
    full_description = HTMLField("Полное описание", blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Бренд")
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


class ProductSpecType(models.Model):
    """Тип характеристики"""

    name = models.CharField("Название", max_length=150, unique=True)
    is_filter = models.BooleanField("Является фильтром", default=False)
    categories = models.ManyToManyField(Category, verbose_name="Категории, где фильтр будет виден", blank=True,
                                        related_name="categories")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Тип характеристики"
        verbose_name_plural = "Типы характеристик"


class ProductSpec(models.Model):
    """Характеристика"""

    type = models.ForeignKey(ProductSpecType, on_delete=models.CASCADE, blank=False, null=False,
                             verbose_name="Тип характеристики")
    value = models.CharField("Значение", max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    def __str__(self):
        return f"{self.type} - {self.value}"

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class ProductDocument(models.Model):
    """Документ"""

    name = models.CharField("Название", max_length=150)
    file = models.FileField("Документ", upload_to='product/docs', blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Документ товара"
        verbose_name_plural = "Документы товара"
