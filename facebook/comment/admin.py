from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at', 'updated_at', 'parent_comment')
    search_fields = ('content', 'user__username', 'post__title')
    list_filter = ('created_at', 'updated_at', 'post')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    # Filtrer les commentaires par post
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('post', 'user').prefetch_related('replies')


# Enregistrer le modèle Comment avec son interface d'administration
admin.site.register(Comment, CommentAdmin)
