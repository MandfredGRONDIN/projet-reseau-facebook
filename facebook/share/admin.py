from django.contrib import admin
from .models import Share

class ShareAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans l'interface d'administration
    list_display = ('user', 'post', 'share_date', 'created_at')

    # Champs sur lesquels on peut effectuer des recherches
    search_fields = ('user__username', 'post__id')

    # Permet de trier les partages par date de partage
    ordering = ('-share_date',)

    # Ajout d'un filtre pour trier les partages par date
    list_filter = ('share_date',)

    # Affichage de l'ID du post partagé sous forme lisible
    def get_post_id(self, obj):
        return obj.post.id
    get_post_id.short_description = 'Post ID'

# Enregistrer le modèle Share avec l'interface d'administration personnalisée
admin.site.register(Share, ShareAdmin)
