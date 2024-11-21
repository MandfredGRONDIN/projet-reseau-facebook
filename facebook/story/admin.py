from django.contrib import admin
from .models import Story

class StoryAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans l'interface d'administration
    list_display = ('user', 'media_url', 'expiration_date', 'created_at')

    # Champs sur lesquels on peut effectuer des recherches
    search_fields = ('user__username', 'media_url')

    # Permet de trier les stories par date de création
    ordering = ('-created_at',)

    # Ajout d'un filtre pour trier les stories par date d'expiration
    list_filter = ('expiration_date',)

    # Permet de cliquer sur un utilisateur pour voir ses détails
    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'Username'

# Enregistrer le modèle Story avec l'interface d'administration personnalisée
admin.site.register(Story, StoryAdmin)
