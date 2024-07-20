from django.contrib import admin

from .models import PopularQuestion


@admin.register(PopularQuestion)
class PopularQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question")
    list_display_links = ("id", "question")
    save_as = True
    search_fields = ("question",)
