from django.db import models


class PopularQuestion(models.Model):
    """Частый вопрос"""

    question = models.CharField("Вопрос", max_length=200)
    answer = models.TextField("Ответ")

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = "Частый вопрос"
        verbose_name_plural = "Частые вопросы"
