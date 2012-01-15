Django, sqlite et mod_wsgi, attention au piège!
###############################################
:date: 2009-03-14 15:34
:category: django
:tags: sqlite

Tout d'abord, je tiens à préciser que le problème qui suit n'est pas
limité à l'utilisation de django ou de mod\_wsgi.

Le contexte
~~~~~~~~~~~

Utilisation de *SQLite* pour un projet django déployé sur mod\_wsgi:

::

    # settings.py
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = '/opt/mysite/mysite.db'

Et voici les permissions sur le système de fichier:

::

    -rw-rw-rw- 1 ohan ohan 29696 2009-03-14 13:30 mysite.db

Tous les répertoires parents sont eux en *755* (lecture et exécution),
ce qui ne devrait donc poser aucun problème, même pour l'utilisateur
utilisé par les processus apache/mod\_wsgi.

Le problème
~~~~~~~~~~~

Lors de la première tentative d'accès à la base de donnée (par exemple
en accédant à l'administration django), une erreur *500 INTERNAL SERVER
ERROR* est renvoyée, et dans le fichier de log d'apache:

::

    OperationalError: unable to open database file

La solution
~~~~~~~~~~~

Lors de l'accès à un fichier de base de données, *SQLite* va créer un
fichier journal qui lui servira (entre autres) à gérer les accès à cette
base. Plus d'informations sur la page expliquant les méthodes de
vérouillage: `locking in sqlite v3`_.

Pour créer ce fichier, il faut donc que l'utilisateur puisse écrire
dans le répertoire parent.

::

    chmod a+rw /opt/mysite

Ce problème ne devrait se présenter que lors d'un déploiement en
environnement de production pour un projet qui utilise *SQLite*, ou sur
un environnement de test si, comme moi, vous préférez tester sur apache
directement, et non sur le *runserver.*

.. _locking in sqlite v3: http://www.sqlite.org/lockingv3.html
