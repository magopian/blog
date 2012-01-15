Double encodage utf8 : afficher correctement avec python et django
##################################################################
:date: 2010-12-27 16:39
:category: django
:tags: mysql, python

Nous avons vu dans un précédent article qu'il pouvait y avoir des soucis
de `double encodage utf8`_, par exemple pour des textes stockés dans une
base de donnée.

Imaginons, un court instant (parce que plus longtemps que ça, ce serait
bien trop douloureux hein ;)), que nous ayons une base de donnée avec
certains champs de certaines tables qui sont doublement encodés en
UTF-8, par exemple le champ *name*.

Le problème
~~~~~~~~~~~

Voici à quoi ressemblerait le modèle Django d'une telle table :

::

    class Foo(models.Model):
        name = models.CharField(max_length=70)

        def __unicode__(self):
             return self.name

Et voici un exemple d'affichage (dans l'admin) du nom d'un tel modèle :
*HelicoptÃ¨re*

En effet, *Hélicoptère*, représenté en utf8 par *Helicopt\\xe8re*, est
stocké en *latin1* par MySQL, et donc renvoyé (doublement) encodé en
utf8 sous la forme *Helicopt\\xc3\\xa8re*.

La solution
~~~~~~~~~~~

Puisque la donnée est doublement encodée, il suffit de la décoder une
fois :

::

    >>> f = Foo.objects.get(name__startswith='Helico')
    >>> f.name
    u'Helicopt\xc3\xa8re'
    >>> f.name.encode('latin1')
    'Helicopt\xc3\xa8re'
    >>> f.name.encode('latin1').decode('utf8')
    u'Helicopt\xe8re'

Et le tour est joué!

Un affichage (presque) propre avec django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans django, il est possible de spécifier une méthode *\_\_unicode\_\_*
sur un modèle, pour gérer son affichage par défaut, qui est utilisé
notamment dans l'affichage des listes d'objets d'un modèle, dans
l'administration.

Nous pouvons donc modifier la méthode de notre modèle indiqué en début
de cet article :

::

        def __unicode__(self):
             return self.name.encode('latin1').decode('utf8')

Mais... tout n'est pas parfait
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il faut penser aux points suivants :

#. il faut bien utiliser *\_\_unicode\_\_* à la place de *name* partout
   où c'est possible, par exemple si on spécifie un *list\_display* dans
   le ModelAdmin
#. lorsqu'on éditera l'objet, le *name* doublement encodé apparaîtra, et
   si on le modifie manuellement pour s'afficher correctement, on aura
   une incohérence dans la table, avec des données doublement encodées,
   et d'autres stockées correctement

Une autre méthode
~~~~~~~~~~~~~~~~~

Il est possible de spécifier des options lors de la connexion à la DB
MySQL, avec django, pour lui demander d'utiliser le charset *latin1*. Vu
que django lui-même ne parle qu'en utf8, demander à MySQL des données en
*latin1* revient à lui demander de ne pas ré-encoder la donnée qu'il
pense être stockée en *latin1*, mais qui sera ensuite correctement
affichée par django *:*

::

    DATABASES = {
        'hack': {
            'NAME': 'bar',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'baz',
            'PASSWORD': 'bizbaz',
            'HOST': 'localhost',
            'PORT': '',
            'OPTIONS': {
                'charset': 'latin1',
                'use_unicode': False,
            },
        },
    }

L'avantage ici est qu'il n'y a pas besoin d'avoir un traitement
spécifique des données, par exemple dans la méthode *\_\_unicode\_\_*,
et que toutes les données lues seront dé-doublement-encodées (!?).

Le gros inconvénient est que toutes les tables subiront le même
traitement, même celles qui ont un encodage et stockage correct.
L'utilisation d'un routeur et d'une deuxième entrée dans les *DATABASES*
uniquement pour les tables ayant un soucis n'étant pas une solution
durable non plus, car celà limite les relations entre tables.

Et tant qu'à faire dans le crade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La solution la plus dangereuse serait d'avoir un traitement "par
défaut" de toutes les données qu'on veut afficher, pour :

#. régler le problème du double-encodage si il y en a un
#. afficher la donnée brute si on ne peut pas dé-double-encoder

Exemple :

::

        def __unicode__(self):
            try:
                return self.name.encode('latin1').decode('utf8')
            except:
                return self.name

On ne se pose alors plus la question de la cohérence des données et de
leur encodate et stockage dans la base de donnée, mais on se met à dos
une énorme dette technique : le développement du traitement spécifique
de toutes les colonnes de toutes les tables le nécessitant peut être
titanesque, et bien plus lourd que la correction du problème à la base.

Conclusion
~~~~~~~~~~

Rien ne vaut une DB saine, ses tables étant toutes encodées
correctement. Si vous commencez à utiliser des workarounds ou hacks
divers, vous vous en mordrez les doigts (il me manque déjà plusieurs
phalanges, croyez-moi).

La `dette technique`_ (métaphore inventée par Ward Cunningham) est une
plaie dont il faut se préserver au maximum, et qu'il faut rembourser le
plus tôt possible.

.. _double encodage utf8: ./mysql-mysqldump-et-php-convertir-de-latin1-vers-utf8.rtml
.. _dette technique: http://en.wikipedia.org/wiki/Technical_debt
