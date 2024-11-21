import json
import os
import django
import random  # Ajout du module random
from django.core.management import execute_from_command_line
from django.conf import settings
from django.core.files import File  # Ajout de l'importation de File

# Assurez-vous que Django est configuré
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facebook.settings")  # Remplacez par le nom de votre projet
django.setup()

# Importez les modèles nécessaires
from django.contrib.auth.models import User
from post.models import Post
from profile.models import Profile
from comment.models import Comment
from friendship.models import Friendship
from story.models import Story
from reaction.models import Reaction
from share.models import Share  # Ajoutez l'importation du modèle Share

def import_data_from_json(json_file):
    # Ouvrir et charger le fichier JSON
    with open(json_file, 'r') as file:
        data = json.load(file)

    posts_created = {}
    users_created = {}
    friendships_created = []
    reactions_created = []
    shares_created = []
    stories_created = []

    # Liste des noms d'images disponibles
    available_images = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg']

    # Insérer les données dans la base de données
    for entry in data:
        model_name = entry['model']
        fields = entry['fields']
        pk = entry.get('pk')

        if model_name == 'auth.user':
            # Crée un utilisateur avec les champs nécessaires
            user = User.objects.create_user(
                username=fields['email'],  # Utilise l'email comme username
                email=fields['email'],
                first_name=fields.get('first_name', ''),
                last_name=fields.get('last_name', ''),
                password=fields['password']  # Le mot de passe sera géré par set_password plus tard
            )
            user.set_password(fields['password'])
            user.save()
            print(f"Utilisateur créé : {user.username}")

            # Sauvegarde l'utilisateur dans le dictionnaire avec son pk
            users_created[pk] = user

            # Crée également un profil pour cet utilisateur
            profile = Profile.objects.create(user=user)

            # Ajoute la biographie si elle existe dans le fichier JSON
            if 'bio' in fields:
                profile.bio = fields['bio']
            
            # Choisis une image de profil aléatoire parmi les images disponibles
            random_image = random.choice(available_images) 
            image_path = os.path.join(settings.MEDIA_ROOT, 'profile_pictures', random_image)

            # Assigne l'image de profil
            with open(image_path, 'rb') as image_file:
                profile.profile_picture.save(random_image, File(image_file), save=True)

            profile.save()
            print(f"Profil créé pour : {user.username}, image de profil assignée : {random_image}")

        elif model_name == 'post.post':
            # Crée un post
            user_id = fields['user']
            user = users_created.get(user_id)  # Récupère l'utilisateur créé pour ce post
            if not user:
                user = User.objects.get(id=user_id)  # Si l'utilisateur n'est pas dans le dictionnaire, récupère-le de la DB

            post = Post.objects.create(
                user=user,  # Associe l'utilisateur au post
                content=fields['content'],
                media_url=fields.get('media_url', '')
            )
            posts_created[pk] = post  # Sauvegarde le post créé dans le dictionnaire avec son pk
            print(f"Post créé : {post.content}")

        elif model_name == 'friendship.friendship':
            # Crée une amitié
            user1_id = fields['user1']
            user2_id = fields['user2']
            status = fields['status']

            user1 = users_created.get(user1_id) or User.objects.get(id=user1_id)
            user2 = users_created.get(user2_id) or User.objects.get(id=user2_id)

            # Si l'amitié n'existe pas déjà, crée-la
            friendship, created = Friendship.objects.get_or_create(
                user1=user1,
                user2=user2,
                defaults={'status': status}
            )
            if created:
                friendships_created.append(friendship)
                print(f"Amitié créée entre {user1.username} et {user2.username} ({status})")

        elif model_name == 'comment.comment':
            # Crée un commentaire
            post_id = fields['post']
            post = posts_created.get(post_id)  # Essaie de récupérer le post dans le dictionnaire
            if not post:  # Si le post n'est pas dans le dictionnaire, récupère-le de la DB
                post = Post.objects.get(id=post_id)
            
            user = users_created.get(fields['user'])  # Récupère l'utilisateur du dictionnaire
            if not user:  # Si l'utilisateur n'est pas dans le dictionnaire, récupère-le de la DB
                user = User.objects.get(id=fields['user'])

            comment = Comment.objects.create(
                user=user,
                post=post,
                content=fields['content'],
                media_url=fields.get('media_url', '')
            )
            print(f"Commentaire ajouté : {comment.content}")

        elif model_name == 'reaction.reaction':
            # Crée une réaction
            user_id = fields['user']
            post_id = fields.get('post')
            comment_id = fields.get('comment')
            reaction_type = fields['type']

            user = users_created.get(user_id) or User.objects.get(id=user_id)
            post = posts_created.get(post_id) if post_id else None
            comment = Comment.objects.get(id=comment_id) if comment_id else None

            # Crée la réaction sur le post ou le commentaire
            reaction = Reaction.objects.create(
                user=user,
                post=post,
                comment=comment,
                type=reaction_type
            )
            reactions_created.append(reaction)
            print(f"Réaction ajoutée : {reaction.user.username} - {reaction.get_type_display()}")

        elif model_name == 'share.share':
            # Crée un partage
            user_id = fields['user']
            post_id = fields['post']

            user = users_created.get(user_id) or User.objects.get(id=user_id)
            post = posts_created.get(post_id) or Post.objects.get(id=post_id)

            share = Share.objects.create(
                user=user,
                post=post
            )
            shares_created.append(share)
            print(f"Post partagé par {share.user.username} sur {share.share_date}")

        elif model_name == 'story.story':
            # Crée une story
            user_id = fields['user']
            user = users_created.get(user_id) or User.objects.get(id=user_id)

            story = Story.objects.create(
                user=user,
                media_url=fields['media_url'],
                expiration_date=fields['expiration_date']
            )
            stories_created.append(story)
            print(f"Story créée par {story.user.username} avec expiration à {story.expiration_date}")

def main():
    json_file = 'fake_data.json'  # Spécifiez ici le chemin de votre fichier JSON
    import_data_from_json(json_file)

if __name__ == '__main__':
    main()
