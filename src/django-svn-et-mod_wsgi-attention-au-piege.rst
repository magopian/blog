Django svn et mod_wsgi, attention au piège!
###########################################
:date: 2009-02-17 22:34
:category: django

Scénario
~~~~~~~~

Notre cher utilisateur *biboul* se décide à installer la version de
développement de django, que nous appellerons django-trunk, comme
indiqué sur la page `How To Install Django`_.

Il lance donc les commandes suivantes:

::

    biboul@laptop:~$ svn co http://code.djangoproject.com/svn/django/trunk/ django-trunk
    biboul@laptop:~$ ln -s `pwd`/django-trunk/django /usr/lib/python2.5/site-packages/django
    biboul@laptop:~$ ln -s `pwd`/django-trunk/django/bin/django-admin.py /usr/local/bin

Il a bien entendu

#. `configuré`_ son serveur apache pour utiliser le module WSGI
#. `testé`_ avec le script wsgi "hello world" que la configuration était bonne
#. `modifié`_ le script wsgi de manière à utiliser son application django *mysite*

Le problème
~~~~~~~~~~~

Lors de la première requête à son application *mysite*, une belle "*500
Internal Server Error*" s'affiche, avec les messages d'erreurs suivants
dans le fichier */var/log/apache2/error\_log*:

::

    ...  mod_wsgi (pid=5803): Target WSGI script '/opt/tcs/tcs.wsgi' cannot be loaded as Python module.
    ...  mod_wsgi (pid=5803): Exception occurred processing WSGI script '/opt/tcs/tcs.wsgi'.
    ...  Traceback (most recent call last):
    ...       File "/opt/tcs/tcs.wsgi", line 6, in <module>
    ...           import django.core.handlers.wsgi
    ...  ImportError: No module named django.core.handlers.wsgi

Mais pourquoi donc, alors qu'un *import django.core.handlers.wsgi*
fonctionne correctement, que ce soit dans l'interpréteur ou dans le
shell django?

La réponse
~~~~~~~~~~

Tout simplement parce que le répertoire *django-trunk* (dont notre cher
utilisateur *biboul* a fait un lien symbolique dans le
répertoire*site-packages*) n'est pas accessible à un utilisateur
différent, si il n'est pas dans le même *group*.

Or, par défaut et sur la plupart des distributions Linux, les processus
*apache* sont lancé avec un utilisateur limité (*www-data*, *www* ou
encore *apache*).

La solution
~~~~~~~~~~~

Un simple *chmod 755* des répertoires parents au répertoire
*django-trunk* est suffisant pour régler ce problème.

Une autre solution, plus propre et sécurisée, serait de placer le
répertoire *django-trunk* dans le répertoire */opt*, et de modifier les
liens symboliques pour utiliser ce nouvel emplacement.

.. _How To Install Django: http://docs.djangoproject.com/en/dev/topics/install/#installing-development-version
.. _configuré: http://code.google.com/p/modwsgi/wiki/QuickInstallationGuide
.. _testé: http://code.google.com/p/modwsgi/wiki/QuickConfigurationGuide
.. _modifié: http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
