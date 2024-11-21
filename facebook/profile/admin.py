from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans l'interface d'administration
    list_display = ('user', 'bio', 'profile_picture', 'short_bio')

    # Ajout de filtres pour la recherche par utilisateur
    search_fields = ('user__username', 'user__email', 'bio')

    # Ajout d'un champ personnalisé pour afficher une version courte de la bio
    def short_bio(self, obj):
        # Vérifie si la bio existe et n'est pas None
        if obj.bio:
            return obj.bio[:50] + ('...' if len(obj.bio) > 50 else '')
        return "No bio available"
    
    short_bio.short_description = 'Short Bio'

    # Permet de trier par utilisateur, en fonction de la date d'adhésion
    ordering = ('user__date_joined',)

# Enregistrer le modèle Profile avec l'interface d'administration personnalisée
admin.site.register(Profile, ProfileAdmin)
