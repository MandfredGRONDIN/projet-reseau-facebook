###############################################################################
# Context
###############################################################################
export APP = facebook
export ENV = $(shell [ -f ../ENV ] && cat ../ENV || echo pro)
export VER = $(shell [ -f ./VERSION ] && cat ./VERSION || echo unknown)
export TZ = $(shell [ -f ../TZ ] && cat ../TZ || echo Europe/Paris)
export UID = $(id -u)
export GID = $(id -g)

###############################################################################
# Global vars
###############################################################################
export SHORT_ENV = $(shell echo ${ENV} | cut -c1-3)

###############################################################################
# Make vars
###############################################################################
COMPOSE=docker-compose -p ${APP}-${SHORT_ENV} -f ./docker-compose.yml

# Default target
default: build up

# Utils targets
mkdata:
	mkdir -p ../data && chmod 777 ../data
	mkdir -p ../data/logs  && chmod 777 ../data/logs
	
# Compose shortcuts
build:
	${COMPOSE} build

up:
	${COMPOSE} up -d

down:
	${COMPOSE} down

logs:
	${COMPOSE} logs -f

# Commandes pour les migrations
migrate:
	${COMPOSE} run facebook python manage.py makemigrations
	${COMPOSE} run facebook python manage.py migrate

# Créer un superutilisateur Django
createsuperuser:
	${COMPOSE} run facebook python manage.py createsuperuser

# Commande pour importer des données fake depuis un fichier JSON
import_fake_data:
	${COMPOSE} run --rm facebook python /app/import_fake_data.py

# Pour exécuter l'application
run: 
	${COMPOSE} up

# Commande pour lancer les tests Django
test:
	${COMPOSE} run facebook python manage.py test

###############################################################################
# Clean up
###############################################################################
clean:
	docker-compose down --volumes --remove-orphans
