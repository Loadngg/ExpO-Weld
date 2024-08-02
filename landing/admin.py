from django.contrib import admin

from .models import PopularQuestion, YouTubeVideo, Callback


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


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ("id", "datetime", "full_name", "phone_number", "article")
    list_display_links = ("id", "datetime", "full_name", "phone_number")
    search_fields = ("full_name", "phone_number", "article")
    list_filter = ["datetime"]
    ordering = ['-datetime']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
