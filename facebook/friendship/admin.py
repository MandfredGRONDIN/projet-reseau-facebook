from django.contrib import admin
from .models import Friendship

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user1__username', 'user2__username', 'status')
    ordering = ('-created_at',)
    
    # Personnaliser la forme d'affichage du statut dans l'admin
    def get_status_display(self, obj):
        return obj.get_status_display()

    get_status_display.short_description = 'Status'

    # Personnaliser les actions dans l'admin
    actions = ['accept_friendship', 'reject_friendship']

    def accept_friendship(self, request, queryset):
        queryset.update(status=Friendship.ACCEPTED)

    def reject_friendship(self, request, queryset):
        queryset.update(status=Friendship.REJECTED)

    # Enregistre la nouvelle interface d'admin
    accept_friendship.short_description = 'Accepter la demande d\'amitié'
    reject_friendship.short_description = 'Rejeter la demande d\'amitié'


# Enregistrer le modèle Friendship avec son interface d'administration personnalisée
admin.site.register(Friendship, FriendshipAdmin)
