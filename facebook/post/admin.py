from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la page de liste des posts
    list_display = ('user', 'content', 'created_at', 'updated_at', 'media_url', 'short_content')
    
    # Ajout de filtres pour trier les posts par utilisateur et date de création
    list_filter = ('user', 'created_at', 'updated_at')
    
    # Ajouter un champ de recherche pour rechercher dans le contenu et le nom d'utilisateur
    search_fields = ('user__username', 'content')
    
    # Définir un tri par défaut
    ordering = ('-created_at',)
    
    # Ajouter des actions personnalisées
    actions = ['delete_selected_posts']

    # Fonction pour afficher un aperçu du contenu (afin de ne pas afficher des contenus trop longs)
    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    short_content.short_description = 'Content Preview'

    # Action personnalisée pour supprimer les posts sélectionnés
    def delete_selected_posts(self, request, queryset):
        queryset.delete()

    delete_selected_posts.short_description = "Delete selected posts"

# Enregistrer le modèle Post avec l'interface d'administration personnalisée
admin.site.register(Post, PostAdmin)
