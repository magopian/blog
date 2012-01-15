Contribuer à Django, premiers pas (les outils, l'environnement) 
###############################################################
:date: 2011-04-25 13:52
:category: django

Ceci est le deuxième article dans la série, le premier étant `Contribuer à Django, premiers pas (revue de tickets)`_.

Maintenant qu'on a compris le *flow* entre les différents états de
tickets, et les *flags* associés, passons aux choses sérieuses : la
soumission d'un patch !

Mais avant de pouvoir soumettre un patch, il faut avoir son
environnement prêt, c'est à dire une version récente du *trunk*, un
projet brouillon et une application de test, et enfin les différentes
dépendances nécessaires.

La démarche expliquée ici utilise *git*, qui semble être la méthode la
plus répandue (autre que *svn*, que je connais moins bien).

Créer son virtualenv
~~~~~~~~~~~~~~~~~~~~

Tout le monde sait comment créer un `virtualenv`_ de nos jours,
n'est-ce pas ? Pour ceux qui ne connaissent pas encore cet excellent
outil, je leur conseille vivement de s'y intéresser, ainsi qu'à
`pip`_, et à `virtualenvwrapper`_ pour les fainéant (et `la fainéantise`_, `c'est bien`_).

::

    $ mkvirtualenv scratch

Créer son projet
~~~~~~~~~~~~~~~~

Il est `recommandé`_ d'avoir un squelette de projet Django, pour
pouvoir démarrer plus rapidement, sans avoir à répéter sans cesse les
mêmes actions. Celui que j'utilise pour mes projets réels `se trouve
ici`_, et je vous conseille d'avoir le votre, avec vos propres réglages
!

Dans le cas de la contribution à Django, j'ai créé un autre squelette,
`django\_scratch`_, qui n'a pas d'autres applications installées que
celles par défaut, en rajoutant l'admin et une application de test vide.

::

    $ cd ~/projects/
    $ hg clone https://magopian@bitbucket.org/magopian/django_scratch scratch
    $ cd scratch

Cloner le repository de django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il existe un miroir du *svn* de Django `sur github`_ que nous allons
utiliser, mais vu que je suis super sympa, je vous l'ai déjà mis dans
les *requirements* de *pip* :

::

    $ pip install -r pip_requirements.txt

Pour le même prix, *sphinx* (qui dépends de *pygments*) sera installé
par la même occasion, outil indispensable pour pouvoir contribuer à la
documentation.

Finaliser
~~~~~~~~~

Vous avez normalement tout ce qu'il faut pour débuter votre carrière de
contributeur !

Une base de donnée sqlite
^^^^^^^^^^^^^^^^^^^^^^^^^

Par défaut, c'est le moteur utilisé, car plus rapide pour les tests et
surtout beaucoup plus simple à configurer. Pour faciliter les choses, il
y a déjà *scratch.db.save* qui est une base initialisée avec les tables
nécessaires à Django, et même un admin (login: admin, pass: admin).

Pour l'utiliser, ou la ré-utiliser pour revenir à la configuration de
base :

::

    $ cp scratch.db.save scratch.db

Il y a aussi *mysql\_settings.py* et *postgresql\_settings.py* qui sont
là pour les cas où le moteur de base de données est important et doit
être testé. Il vous suffit d'écraser *settings.py* avec le fichier de
votre choix, et de créer un fichier *creds.py* qui contient (à modifier
avec vos user/pass bien entendu) :

::

    # creds.py
    MY_CREDS = {'user': 'foo', 'pass': 'bar'}
    PG_CREDS = {'user': 'foo', 'pass': 'bar'}

Une application de test
^^^^^^^^^^^^^^^^^^^^^^^

Cette application est constituée d'un modèle *Foo* avec un seul champ
*name*, l'*AdminModel* qui va avec, un *urls.py* et *views.py* basiques.

Le but est d'avoir le minimum nécessaire à la reproduction de la
majorité des bugs, et ce avec un minimum de travail. N'oubliez pas de
faire un *syncdb* pour que le(s) modèle(s) soi(en)t créé(s) !

Le trunk de Django
^^^^^^^^^^^^^^^^^^

Il a été cloné directement dans le répertoire *src* de votre
*virtualenv*. Si vous avez suivi exactement tout ce qui a été indiqué
dans ce billet, vous devriez pouvoir créer un lien symbolique du
répertoire de Django à un endroit plus pratique et accessible (vous
allez devoir y modifier des fichiers régulièrement) :

::

    $ ln -s ~/.virtualenvs/scratch/src/django ~/projects/

De la documentation en sphinx
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Elle se trouve directement dans le répertoire *docs* du *trunk* de
Django, et pour la générer, rien de plus simple :

::

    $ cd ~/projects/django/docs
    $ make html

S'ensuit la génération de tous les fichiers *html* de la documentation
de Django, que vous pourrez visualiser et contrôler en pointant votre
navigateur sur le répertoire ``_build/html/`` :

`file:///chemin/vers/projects/django/docs/\_build/html/index.html`_

Bon, et donc, quand est-ce qu'on contribue ? Nous verrons ça dans le
prochain article, promis !


.. _Contribuer à Django, premiers pas (revue de tickets): ./contribuer-a-django-premiers-pas-revue-de-tickets.html
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _la fainéantise: http://mathieu.agopian.info/djangocong/dplf.html
.. _c'est bien: http://vimeo.com/11381846
.. _recommandé: http://mathieu.agopian.info/djangocong/dplf.html
.. _se trouve ici: https://bitbucket.org/magopian/django_base/overview
.. _django\_scratch: https://bitbucket.org/magopian/django_scratch
.. _sur github: https://github.com/django/django
.. _`file:///chemin/vers/projects/django/docs/\_build/html/index.html`: file:///chemin/vers/projects/django/docs/_build/html/index.html
