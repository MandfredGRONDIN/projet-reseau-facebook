from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Reaction
from post.models import Post

class AddReactionView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)

        # Vérifier si l'utilisateur a déjà réagi à ce post
        existing_reaction = Reaction.objects.filter(
            user=request.user,
            post=post
        ).first()

        reaction_type = request.POST.get('type', 'like') 

        if existing_reaction:
            if existing_reaction.type == reaction_type:
                # Si la réaction est identique, on la supprime
                existing_reaction.delete()
                return JsonResponse({'message': 'Réaction supprimée', 'liked': False})

            else:
                # Si la réaction est différente, on la met à jour
                existing_reaction.type = reaction_type
                existing_reaction.save()
                return JsonResponse({'message': 'Réaction mise à jour', 'liked': True, 'type': reaction_type})

        # Sinon, on crée une nouvelle réaction
        reaction = Reaction.objects.create(
            user=request.user,
            post=post,
            type=reaction_type
        )

        return JsonResponse({'message': 'Réaction ajoutée', 'liked': True, 'type': reaction_type})
