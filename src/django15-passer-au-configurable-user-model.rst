#############################################
Django1.5 : passer au Configurable User Model
#############################################
:date: 2013-04-16 14:13
:category: django


Depuis la version 1.5 de Django, il est possible d'utiliser un `Configurable
User Model`_ en lieu et place de ``django.contrib.auth.User``.

Cela permet, par exemple, de se passer de *proxy model* ou encore de fusionner
le profil avec l'utilisateur, pour éviter des *join* dans les requêtes SQL.

Très pratique, et facile à mettre en place sur un projet qui commence juste,
mais comment gérer ça en utilisant South_ sur un projet déjà bien en place ?

Le but est donc de fusionner l'utilisateur et le profil, avec pour
aide/contrainte d'utiliser South, autant sur des plateformes existantes
(serveur de production, de pré-production) que sur les plateformes de
développement : donc les migrations doivent fonctionner sur une création de
base, tout autant que sur une migration simple.

Nous allons détailler plusieurs stratégies.

.. _Configurable User Model: https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#auth-custom-user
.. _South: http://south.aeracode.org/


Contexte
========

Notre projet utilise depuis longtemps un *proxy model* sur l'utilisateur, ne
rajoutant que quelques méthodes. Toutes les données liées à l'utilisateur sont
par ailleurs stockées dans un profil, qui est utilisé par le biais de
``get_profile()`` (et le *setting* ``AUTH_PROFILE_MODULE``).


.. code-block:: python

    from django.db import models
    from django.contrib.auth.models import User


    class RH2User(User):

        class Meta:
            proxy = True

        ...


    class RH2UserProfile(models.Model):
        some_field = models.CharField(max_length=50)
        some_other_field = models.BooleanField()

        def some_method(self):
            ...


Le résultat, une fois le profil fusionné avec l'utilisateur :

.. code-block:: python

    from django.db import models
    from django.contrib.auth.models import AbstractUser


    class RH2User(AbstractUser):
        some_field = models.CharField(max_length=50)
        some_other_field = models.BooleanField()

        def some_method(self):
            ...

Ne pas oublier de fusionner les *managers*, les méthodes ``save()``, et de
dédoublonner les champs ayant le même nom (dans notre cas,
``RH2UserProfile.last_login`` a été renommé en ``RH2User.previous_last_login``,
étant donné que le modèle ``auth.User`` d'origine avait déjà un champ
``last_login``).

Il faut par ailleurs rechercher et remplacer le cas échéant toutes les
occurrences de :

* ``RH2UserProfile``
* ``get_profile()``
* ``rh2userprofile__``
* ``.user``

La problématique
================

À partir du moment où le paramètre ``AUTH_USER_MODEL`` est renseigné :

* les tables ``auth_user``, ``auth_user_user_permissions``,
  ``auth_user_groups`` ne sont plus automatiquement crées par un ``python
  manage.py syncdb``
* toutes les migrations South existantes sur des modèles ayant une *ForeignKey*
  ou *Many to Many* ne passerons plus tel quel

Il y a donc principalement deux stratégies pour les migrations South, une fois
qu'on a notre modèle ``RH2User`` complet (et non plus *proxy*) ainsi que
``AUTH_USER_MODEL = 'account.RH2User'`` dans les paramètres :

- Modifier la migration initiale de l'app *account*, puis toutes les
  migrations suivantes ainsi que les migrations des app ayant une relation
  avec l'utilisateur pour qu'elles se basent sur ``account_rh2user`` au lieu
  de ``auth_user``
- Rajouter la création de la table ``auth_user``,
  ``auth_user_user_permissions`` et ``auth_user_groups`` dans la migration
  initiale de l'app contenant le modèle complet, puis rajouter une migration
  qui va renommer la table ``auth_user`` en ``account_rh2user``

Dans les deux cas, il faudra être attentif à l'ordre d'exécution des
migrations : toutes les applications ayant une relation avec l'utilisateur
devront dépendre de la migration initiale qui crée la table ``auth_user`` ou
``account_rh2user``.

Dans le deuxième cas, il faudra de plus que la première des migration suivant
le renommage, pour chaque application, dépende de cette migration.


Création de account_rh2user et modification des migrations
==========================================================

Le plus simple est de créer une migration de schéma pour avoir le code
nécessaire à la migration ``0001_initial`` de l'application account :

::

    $ python manage.py schemamigration account

Il suffit alors de recopier le code de la migration créée, de le rajouter au
fichier ``account/migrations/0001_initial.py``, puis de supprimer cette
nouvelle migration qui ne sera pas utilisée.

Il faut ensuite modifier chacune des migration, en prenant exemple sur ce qui a
été fait sur django-oauth2-provider_.

.. _django-oauth2-provider:
    https://github.com/caffeinehit/django-oauth2-provider/pull/18/files

Il reste la problématique de la migration des serveurs déjà en production (qui
ont déjà un certain nombre de migrations effectuées, et une base de donnée à
conserver). Une solution serait de créer une migration de données et de tester
l'existence de la table ``auth_user``, et le cas échéant de dupliquer les
données dans la table ``account_rh2user``.

N'ayant pas testé cette solution, je ne peux la garantir.


Création de auth_user puis renommage
====================================

C'est la solution que nous avons choisi, étant donné le nombre de migrations
que nous avons (près d'une centaine), qu'il aurait fallu modifier une à une,
ainsi que le soucis de migration des serveurs déjà en production.

Il faut dans l'ordre :

- créer les tables ``auth_user``, ``auth_user_user_permissions`` et
  ``auth_user_groups`` dans la migration ``0001_initial`` de account
- créer une migration dans account qui renomme la table ``auth_user`` en
  ``account_rh2user``
- créer une migration dans account qui rajoute les champs du modèle profil à
  l'utilisateur
- créer une migration de données pour dupliquer toutes les données de profil
  dans la table ``account_rh2user``
- pour chaque application ayant une relation vers l'utilisateur, la prochaine
  migration créée devra dépendre de la migration qui renomme la table


Conclusion
==========

Le plus compliqué dans toute cette histoire est la gestion de dépendances entre
les migrations.

Une autre solution non évoquée aurait été de repartir de 0 pour les
migrations : supprimer toutes les migrations existantes, ainsi que la table
``south_migrationhistory``, puis reconvertir toutes les applications à South :

::

    $ python manage.py convert_to_south ....

L'avantage est qu'il n'y a alors aucun soucis de dépendances entre les
migrations, et qu'on repars de quelque chose de propre.

Les inconvénients sont multiples : gérer une migration (à la main?) pour les
plateformes en cours d'utilisation, impossibilité de retourner en arrière
automatiquement, perte de l'historique...

Il y a une autre possibilité (à tester !) qui consiste à spécifier l'attribut
``db_table = 'auth_user'`` dans la *Meta* de notre nouveau modèle ``RH2User``,
pour qu'il utilise exactement la même table. En théorie, il n'y a alors pas
besoin de migration, mais il reste à gérer la fusion du profil dans
l'utilisateur.
