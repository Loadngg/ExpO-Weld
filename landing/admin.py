from django.contrib import admin

from .models import PopularQuestion, YouTubeVideo


@admin.register(PopularQuestion)
class PopularQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question")
    list_display_links = ("id", "question")
    save_as = True
    search_fields = ("question",)


@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("id", "name")
    save_as = True
    search_fields = ("name", "url")
