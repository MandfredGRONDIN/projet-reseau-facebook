# Projet Réseau Django

## Description
Ce projet est une application web développée avec le framework Django. Elle permet de gérer un réseau social (clone de facebook) simple où les utilisateurs peuvent créer des profils, publier des messages et interagir avec d'autres utilisateurs.

## Prérequis
- Docker
- Make

## Installation
1. Clonez le dépôt :
    ```bash
    git clone https://github.com/MandfredGRONDIN/projet-reseau-facebook.git
    cd facebook
    ```

2. Créez un fichier `.env` en vous basant sur le fichier `.envexample` :
    ```bash
    cp .envexample .env
    ```

3. Créez un dossier `media/profile_pictures` et ajoutez-y 5 images nommées `image1.jpg`, `image2.jpg`, `image3.jpg`, `image4.jpg`, `image5.jpg` :
    ```bash
    mkdir -p media/profile_pictures
    # Ajoutez les images dans le dossier media/profile_pictures
    ```

4. Construisez l'application avec Docker :
    ```bash
    make
    ```

5. Appliquez les migrations de la base de données :
    ```bash
    make migrate
    ```

6. Créez un super utilisateur pour accéder à l'interface d'administration :
    ```bash
    make createsuperuser
    ```

7. Importez des données factices pour tester l'application :
    ```bash
    make import_fake_data
    ```

## Utilisation
- Accédez à l'application via `http://localhost:8000/`.
- Connectez-vous à l'interface d'administration via `http://localhost:8000/admin/`.

## Fonctionnalités
- Création/Supression de profils utilisateurs
- Possibilité de modifier la photo de profil et la bio
- Publication de post
- Ajout de commentaire sur les posts
- Ajout de reaction sur les posts
- Partage des posts
- Ajout/Visualisation de story
- Ajout/Supression d'amis

## Auteurs
- [Mandfred GRONDIN](https://github.com/MandfredGRONDIN)
