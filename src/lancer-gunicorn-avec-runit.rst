lancer gunicorn avec runit
##########################
:date: 2010-02-10 11:37
:category: django
:tags: web, runit

**ATTENTION** votre serviteur a fait le test pour vous sur une ubuntu:
après avoir installé ``runit`` et ``runit-run``, le système ne démarre plus.
Pour suivre les étapes de ce billet, il ne faut pas installer
``runit-run``, qui ne doit être installé que lorsque l'on souhaite
remplacer totalement le système d'initialisation (et cela demande plus
de configuration qu'une simple installation du paquet).

Pour les malheureux qui ont fait les frais de la première version de
ce billet (demandant d'installer ``runit-run``), je ne peux que m'excuser
platement, et vous fournir la méthode "au secours rescue moi!":

`récuperer une installation avec un cd ubuntu`_

Une fois chrooté sur la partition root, il vous restera à désinstaller le paquet fautif et
redémarrer:

::

    $ aptitude purge runit-run

Edité le 2010/02/10 à 20:58
                           

--------------

Pour faire suite au précédent billet `gunicorn: un server wsgi ultra simple à utiliser et configurer`_, voici une recette rapide pour lancer
automatiquement (et monitorer) gunicorn avec `runit`_.

Pourquoi runit et pas sysvinit, inittab, upstart, ...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Je vous laisse consulter la page `benefits`_ sur le site officiel pour
vous faire une idée. Pour les personnes ne parlant pas anglais, voici un
bref résumé:

#. Un répertoire par service, contenant un script *run*
#. Un environnement d'exécution propre et prédictible pour chaque
   processus
#. Service de logging (optionnel) qui sera lancé en même temps que le
   processus, et en couvrira toute la durée de vie (redémarrages
   compris!)
#. Très peu encombrant, efficace... et peut complètement remplacer le
   système d'initialisation de votre linux

Utiliser runit avec le système d'initialisation actuel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour nous faciliter la vie, et ne pas avoir à modifier/importer de
nombreux scripts de démarrage pour tous les démons et services déjà
installés, nous allons utiliser runit "avec" le système d'initialisation
actuel.

Installer runit
^^^^^^^^^^^^^^^

::

    $ aptitude install runit

**ATTENTION:** Si vous installez aussi *runit-run*, il vous faut
absolument configurer votre système (`How to replace init`_), et ce,
avant de rebooter (sinon votre système ne démarrera pas, et vous serez
contraint à utiliser une méthode de récupération, comme celle présentée
en tête de ce billet).

Créer un répertoire pour le service gunicorn et son script de lancement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ mkdir /etc/sv/gu-monprojet
    $ vi /etc/sv/gu-monprojet/run

Et voici le contenu du script run

::

    #!/bin/bash
    source /path/to/venv/bin/activate # activer le virtualenv
    cd /path/to/django/project
    exec gunicorn_django -b localhost:8080 --workers=3

Avec la version de gunicorn utilisée pour l'écriture de cet article, il
est nécessaire d'être dans le répertoire du projet django (là ou se
situe le fichier *settings.py*) pour lancer *gunicorn\_django*.

Dans une future version (la modification est dans le *trunk* à l'heure
de l'écriture) il suffira d'indiquer le chemin vers le fichier
*settings.py* comme paramètre à la commande *gunicorn\_django*.

Enfin, ne pas oublier de rajouter les droits d'exécution sur le script
qu'on vient de créer:

::

    $ chmod a+x /etc/sv/gu-monprojet

Indiquer à runit qu'il doit lancer le script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour celà, un simple lien symbolique, et dans les secondes qui suivent
le script sera lancé:

::

    $ ln -s /etc/sv/gu-monprojet /etc/service/

Et c'est tout!
~~~~~~~~~~~~~~

Il suffit maintenant d'en profiter en allant sur http://localhost:8080,
en configurant apache pour proxiser les requêtes directement dessus (cf
le billet `gunicorn: un server wsgi ultra simple à utiliser et
configurer`_), ou encore en utilisant la commande *sv* pour gérer le
service gunicorn:

::

    $ sv status gu-monprojet
    $ sv check gu-monprojet
    $ sv up gu-monprojet
    $ sv down gu-monprojet
    $ sv restart gu-monprojet
    $ sv hup gu-monprojet

    ...

.. _récuperer une installation avec un cd ubuntu: http://www.tenshu.fr/ubuntu/recuperer-une-installation-avec-un-cd-ubuntu/
.. _`gunicorn: un server wsgi ultra simple à utiliser et configurer`: ./gunicorn-un-server-wsgi-ultra-simple-a-utiliser-et-configurer.html
.. _runit: http://smarden.org/runit/
.. _benefits: http://smarden.org/runit/benefits.html
.. _How to replace init: http://smarden.org/runit/replaceinit.html
