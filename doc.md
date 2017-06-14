Création du dossier **Parking**

Dans Parking :

	sudo apt-get install python3-venv
	python3 -m venv myvenv
	source myvenv/bin/activate
	pip install django==1.10.5
	pip install djangorestframework
	pip install markdown
***		error : invalid command 'bdist_wheel' à voir

	pip install django-filter
Création du projet et de l'appli

	django-admin startproject parking .
	python manage.py startapp stationnement
Edition de **settings.py** suivant notes

	python manage.py migrate
Création de **models.py**

	python manage.py makemigrations stationnement
	python manage.py migrate stationnement
Administration

	stationnement/admin.py... (1 ligne par modèle)
	python manage.py createsuperuser (chris)
Création des urls nécessaires
* dans parking (include stationnement.urls )
* dans stationnement

Création des vues basiques et des templates...

Ajout **rest_framework** dans **INSTALLED_APPS** de **settings**
Création de l'appli **api**

    python manage.py startapp api
    
Création **serializer.py**

	from rest_framework import serializers
	from stationnement.models import *

	class ParkSerializer(serializers.HyperlinkedModelSerializer):
		class Meta:
		    model = Parking
		    fields = ('etage', 'numero', 'couvert', 'voiture', 'date_affect')


	class CarSerializer(serializers.HyperlinkedModelSerializer):
		class Meta:
		    model = Voiture
		    fields = ('marque', 'couleur', 'immat', 'proprietaire')
Création des vues

	from rest_framework import viewsets
	from stationnement.models import *
	from api.serializer import *

	# Create your views here.


	class ParkViewSet(viewsets.ModelViewSet):

		queryset = Parking.objects.all()
		serializer_class = ParkSerializer


	class CarViewSet(viewsets.ModelViewSet):

		queryset = Voiture.objects.all()
		serializer_class = CarSerializer

***** L'éditeur signale l'import des classes de "stationnement" non utilisé !!

Ajout des routes à **urls.py** du projet

	from api import views
	from rest_framework import routers

	router = routers.DefaultRouter()
	router.register(r'parking', views.ParkViewSet)
	router.register(r'voiture', views.CarViewSet)

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		url(r'', include('stationnement.urls')),
		url(r'^api/', include(router.urls)),
	]
Lancement du serveur, accès à l'api avec **http://127.0.0.1:8000/api**  
On tombe sur la page par défaut qui indique les routes disponibles.  
Avec voiture, j'ai ajouté deux entrées.

On ajoute l'url pour le login/logout avec les vues par défaut.

	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

Et un setting pour le framework rest qui va restreindre l'accès aux admins

	REST_FRAMEWORK = {
		'DEFAULT_PERMISSION_CLASSES': [
		    'rest_framework.permissions.IsAdminUser',
		],
		'PAGE_SIZE': 10
	}

La commande curl proposée renvoie un code 301

    curl -H 'Accept: application/json; indent=4' -u chris:chrislo42 http://127.0.0.1:8000/api/voiture -v

Création d'un user non admin avec /admin, logout et retour à l'api.  
login avec nouveau user => réponse :  
*"detail": "You do not have permission to perform this action."*

changement dans **settings** : **IsAdminUser** en **IsAuthenticated**.  
droit d'accès ok maintenant.

En incluant :

	permission_classes = (permissions.IsAdminUser,)
dans une vue, on peut interdire l'accès aux users non admin !

Création d'un fichier **permissions.py** dans api.

	from rest_framework import permissions

	class IsStaffOrReadOnly(permissions.BasePermission):

		def has_permission(self, request, view):

			if request.method in permissions.SAFE_METHODS:
            	return True
			if request.user.is_staff:
				return True
			return False

Importation et ajout de la permission dans la vue.  
Maintenant les utilisateurs non Staff ne peuvent pas poster !

Pour la doc, utilisation de **swagger**.

	pip install django_rest_swagger
***		error : invalid command 'bdist_wheel'

ajout dans **settings** de : **'rest_framework_swagger'**
Modification du fichier **urls** :

	from rest_framework_swagger.views import get_swagger_view

	schema_view = get_swagger_view(title='API Parking')
    urlpatterns = [
        ...
        url(r'^api/docs/', schema_view),
        ...

Restriction sur la route **voiture**; on enlève le champ **propriétaire**.  
On crée une autre route, **propriétaire** avec le modèle **voiture** complet
Sérializer, views et url.  
***	Problème dans le browser api, les routes voiture et propriétaire ont la même url !!  
Si on change l'ordre des routes dans urls, c'est la dernière route qui reste.  
C'est en fait le queryset qui pose problème !!!

Contournement du problème :  
Dans la vue **CarViewSet**, on surcharge la méthode **get_serializer_class**.

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return OwnerSerializer
        else:
            return CarSerializer
Suivant le user, on appelle deux sérializers différents.

Ajout aussi d'une surcharge de **get_queryset** pour trier de deux façons.  
Il a fallu ajouter **base_name='voiture'** dans la ligne concernée de urls.

Typiquement, on donne le nom de la route.  
Avec "toto", **base_name** pertube la route **parking**.  
Du coup, il faut alors supprimer le **base_name** et remettre un queryset qui sera surchargé
par la méthode **get_queryset**.

Implémentation de trois niveaux d'authorisation :  
la route **parking** pour tout le monde mais read-only.  
la route **voiture** pour les utilisateurs enregistrés.  
la route **proprietaire** pour les utilisateurs d'un groupe spécial.  
* modif de settings pour les permissions de **IsAuthenticated** en **IsAuthenticatedOrReadOnly**
* **ParkViewSet** avec **permission_classes = IsStaffOrReadOnly**
* création d'une nouvelle classe de permission **IsStaffOrReadOnlyForAuthenticated**

		    def has_permission(self, request, view):

				if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
				    return True
				if request.user.is_staff:
				    return True
				return False
* **CarViewSet** avec **permission_classes = IsStaffOrReadOnlyForAuthenticated**

Ajout de **DjangoFilterBackend**. Déjà installer par pip.  
Ajout dans **settings** **INSTALLED_APPS**  
* Les filtres :  
	Ajout dans la vue **ParkViewSet** de :
	
		from django_filters.rest_framework import DjangoFilterBackend

		filter_backends = (DjangoFilterBackend,)
		filter_fields = ('etage', 'numero')
On voit maintenant un bouton de filtre pour **Parklist**  
idem pour **voiture** filtre sur **marque**.
* Le search :  
	Ajout de l'import **filters** de **rest_framework**  
	Ajout de **filters.SearchFilter** dans **filter_backends**  
	Ajout de **search_fields** avec les champs authorisés
* Le tri :  
	Ajout de **filters.OrderingFilter** dans **filter_backends** (l'import de filters est déjà fait)  
	Ajout de **ordering_fields** avec les champs authorisés

Ajout de plusieurs entrées dans voiture pour dépasser 10.  
La pagination se mets en route automatiquement en fonction de **PAGE_SIZE** dans **settings**.  
Avec **LimitOffsetPagination**, on a un offset et une limite, **PAGE_SIZE** fixe la limite  
Avec **PageNumberPagination**, on a des pages de **PAGE_SIZE**

**DEFAULT_RENDERER_CLASSES** dans **REST_FRAMEWORK** de **settings**  
Mettre d'abord la réponse souhaitée si la requête ne contient pas de *accept* dans le header.  
Dans la plupart des cas ;
* **rest_framework.renderers.JSONRenderer** : la réponse sera dans le format Json
* **rest_framework.renderers.BrowsableAPIRenderer** permet de pouvoir accéder à l'interface wed de l'api.

Pour faire marcher les autorisations avec un groupe spécial créé avec l'admin.  
On récupére la liste des groupes auquel appartiens le demandeur:

	list = request.user.groups.values_list('name', flat=True)
	
Il n'y a plus qu'a tester si le groupe est dans la liste.

Ajout dans **REST_FRAMEWORK** de **settings** de :

    'rest_framework.authentication.BasicAuthentication',
Et essai avec curl d'accès à l'api :

	curl -H 'Accept: application/json; indent=4' -u chris:foui11a$ -L http://127.0.0.1:8000/api/voiture -v
-L pour la redirection des routes  
-v pour verbose

Modification du template **base.html** dans **myvenv/lib/python3.5/site-packages/rest_framework/templates/rest_framework**  
Changement du **title** dans **HEAD** et du titre bandeau avec lien sur l'application


