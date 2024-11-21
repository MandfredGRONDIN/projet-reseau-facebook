from django.contrib import admin
from .models import Reaction

class ReactionAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans l'interface d'administration
    list_display = ('user', 'post', 'comment', 'type', 'created_at', 'updated_at')

    # Champs sur lesquels on peut effectuer des recherches
    search_fields = ('user__username', 'post__content', 'comment__content', 'type')

    # Ajout d'un filtre pour trier par type de réaction
    list_filter = ('type', 'created_at')

    # Permet de trier les réactions par date de création
    ordering = ('-created_at',)

    # Affichage du type de réaction sous forme lisible
    def get_type_display(self, obj):
        return obj.get_type_display()
    get_type_display.short_description = 'Reaction Type'

# Enregistrer le modèle Reaction avec l'interface d'administration personnalisée
admin.site.register(Reaction, ReactionAdmin)
