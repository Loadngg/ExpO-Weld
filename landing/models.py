from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class PopularQuestion(models.Model):
    """Частый вопрос"""

    question = models.CharField("Вопрос", max_length=200)
    answer = models.TextField("Ответ")

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = "Частый вопрос"
        verbose_name_plural = "Частые вопросы"


class YouTubeVideo(models.Model):
    """Видео с youtube"""

    name = models.CharField("Название", max_length=200)
    url = models.URLField("Ссылка на видео")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Видео с youtube"
        verbose_name_plural = "Видео с youtube"


class Callback(models.Model):
    """Заявка на звонок"""

    datetime = models.DateTimeField("Дата/Время", auto_now_add=True)
    full_name = models.CharField(verbose_name="Полное имя", max_length=150, blank=False, null=False)
    phone_number = PhoneNumberField(verbose_name="Телефон", region="RU", max_length=12)
    message = models.TextField(verbose_name="Сообщение", blank=True, null=True)
    article = models.CharField("Артикул товара", max_length=100, default=0)

    def __str__(self):
        return f"Заявка на звонок от {self.full_name} ({self.phone_number}). Артикул {self.article}"

    class Meta:
        verbose_name = "Заявка на звонок"
        verbose_name_plural = "Заявки на звонки"
