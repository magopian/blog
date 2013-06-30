Le miroir PyPI du pauvre
#########################
:date: 2012-04-12 09:59
:category: django

Deux notes pour commencer cet article :

* J'ai présenté ce sujet sous forme de présentation courte (`lightning talk`)
  lors de `Djangocong 2012`_, voici le `support de présentation`_.
* `Carl Meyer`_, qui est une des références en la matière, a lui aussi
  `présenté sur ce sujet`_.


Bonjour ami lecteur. Je vais te conter mon histoire, en me disant que tu es
peut-être toi aussi passé par là, et que cette expérience t'enrichira.

Tout d'abord, le personnage principal : moi. Je suis fainéant (revoir `la
présentation`_ que j'ai donnée à `Djangocong 2010`_ à ce sujet).


Les protagonistes
~~~~~~~~~~~~~~~~~

`pip`_ et `PyPI`_. Si tu ne connais pas ``pip``, l'outil à utiliser pour
installer des paquets python, honte à toi, arrête de lire immédiatement et
documente toi à ce sujet.

Oui, maintenant.

PyPI (le *Python Package Index*) est le site listant et hébergeant la plupart
des paquets, applications et librairies python qui ne sont pas dans la libraire
standard.


L'intrigue
~~~~~~~~~~

Je travaille sur un projet `Django`_, et ayant fait les choses proprement, j'ai
un ficher ``requirements.pip`` listant les noms ou les urls des différents
paquets que j'utilise.

Ce fichier est utilisé par ``pip`` pour installer automatiquement toutes les
dépendances de mon projet, par exemple lors de l'installation d'un nouveau
serveur ou du déploiement de mon projet :

.. code-block:: sh

    pip install -r requirements.pip


Les péripéties
~~~~~~~~~~~~~~

Elles te sont peut-être arrivées à toi aussi :

* PyPI n'est pas accessible au moment nécessaire (voir les solutions proposées
  dans l'excellent `billet de JKM`_)
* Le paquet (ou la version utilisée) a été supprimé de PyPI (`ça arrive`_)
* Une nouvelle version non compatible a été publiée (la parade est simple :
  utiliser ``pip freeze`` pour *épingler* les versions utilisées)

Une solution à tous ces problèmes est d'utiliser un *miroir local* de PyPI, qui
contiendra tous les paquets nécessaires à notre projet, dans leur version
utilisée.

Il y a plusieurs projets qui permettent de faire ça de manière plus ou moins
automatique :

* `Chishop`_
* `Localshop`_
* `crate.io (le projet)`_
* `pep381client`_
* `z3c.pypimirror`_

Mais ça nécessite d'installer et de gérer une application de plus, or, comme je
l'ai précisé, je suis fainéant, et je n'ai pas envie de consacrer une machine
(et une installation de serveur web) pour ça.


Le sauveur
~~~~~~~~~~

``pip`` à la rescousse, avec deux options très pratiques :

``--find-links``
    URL ou chercher des paquets (notre miroir local !)

``--no-index``
    ignorer les index de paquets (comme PyPI), et ne regarder que sur l'URL
    fournie à ``--find-links``

Mais il y a mieux. Il est possible de mettre l'option ``--find-links`` en tout
début du fichier ``requirements.pip`` pour ne pas avoir besoin de l'utiliser en
ligne de commande (et donc ne pas changer nos habitudes, parfait pour un
fainéant ;).

Pour la deuxième option, elle n'est pas reconnue dans le fichier, mais on peut
utiliser l'option ``--index-url`` à la place. On est alors sûr que ``pip``
n'essaiera pas de trouver un meilleur paquet (meilleure note, version plus
récente) sur PyPI.

Maintenant qu'on sait comment utiliser notre miroir local, il ne reste plus
qu'à le créer :

#. Générer la liste exhaustive de tous les paquets et dépendances
#. Les faire télécharger par ``pip`` dans un répertoire
#. Servir ce répertoire avec un serveur web
#. Modifier le fichier ``requirements.pip``


Générer la liste des paquets
----------------------------

Rien de plus simple :

.. code-block:: sh

    pip freeze > freezed.pip


Télécharger les paquets
-----------------------

On le fait faire par ``pip``, ce serait trop long et fastidieux de tout
télécharger (les paquets et leurs dépendances) sur PyPI (ou git, svn,
mercurial, …) manuellement :

.. code-block:: sh

    mkdir pypi
    pip install -r freezed.pip --upgrade --download=pypi --build=pypi


Servir le répertoire avec un serveur web
----------------------------------------

`SimpleHTTPServer`_ à la rescousse :

.. code-block:: sh

    cd pypi
    python -m SimpleHTTPServer

Le miroir est maintenant accessible sur http://localhost:8000.

Il existe sinon une autre méthode qui consiste à fournir directement une URL de
type ``file:///path/to/mirror/folder`` au paramètre ``find-links``. Dans ce
cas, pas besoin de serveur web !


Modifier le fichier requirements.pip
------------------------------------

La dernière étape de notre périple, avant de rentrer voir sa princesse, de
vivre heureux et d'avoir beaucoup beaucoup d'enfants.

Comme nous l'avons vu, il faut placer les deux lignes suivantes en tête du
fichier ``requirements.pip`` :

.. code-block:: pip

    --find-links http://localhost:8000
    --index-url http://localhost:8000

Ayant maintenant notre propre miroir local, il ne faut plus utiliser les URLs
de téléchargement sur git/svn/mercurial/… pour les paquets qu'on ne souhaite
pas réinstaller à chaque fois :

* les paquets devant être réinstallés à partir de leur dépôts VCS à chaque fois
  resteront avec leur URL complète
* les autres paquets installés à l'origine à partir de dépôts n'ont plus besoin
  de leur url : ne conserver que leur nom (la partie après ``#egg=`` dans leur
  URL)
* tous les autres peuvent être listés sans leurs dépendances

Par exemple, si vous avez installé ``django-notification`` de la sorte :

.. code-block:: sh

    pip install -e git+ssh://git@github.com/jtauber/django-notification.git#egg=django_notification:nohlsearch

Il suffira de mettre la ligne suivante dans le fichier ``requirements.pip`` :

.. code-block:: sh

    django-notification


À partir de maintenant, tout appel à la commande suivante ira automatiquement
installer les paquets disponibles dans le répertoire du miroir local (si le
``SimpleHTTPServer`` est lancé bien entendu) :

.. code-block:: sh

    pip install -Ur requirements.pip


Installer un nouveau paquet ou une nouvelle version
---------------------------------------------------

Rien de plus simple : il suffit de télécharger le paquet (ou sa nouvelle
version) dans le répertoire du miroir local.


----


.. target-notes::

.. _`Djangocong 2012`: http://rencontres.django-fr.org/2012/lightning-talks.html#l5
.. _`support de présentation`: http://mathieu.agopian.info/djangocong/2012/miroir_pypi_local_du_pauvre.pdf
.. _`Carl Meyer`: http://oddbird.net/
.. _`présenté sur ce sujet`: http://carljm.github.com/tamingdeps/#1
.. _`la présentation`: http://mathieu.agopian.info/djangocong/dplf.html
.. _`Djangocong 2010`: http://rencontres.django-fr.org/2010/
.. _`pip`: http://pip-installer.org
.. _`PyPI`: http://pypi.python.org/pypi
.. _`Django`: http://djangoproject.com
.. _`ça arrive`: https://groups.google.com/forum/?fromgroups#!topic/pypi/eDxaJwSkaJ0
.. _`billet de JKM`: http://jacobian.org/writing/when-pypi-goes-down/
.. _`crate.io`: http://crate.io
.. _`Chishop`: http://justcramer.com/2011/04/04/setting-up-your-own-pypi-server/
.. _`Localshop`: http://pypi.python.org/pypi/localshop
.. _`crate.io (le projet)`: https://github.com/crateio/crate-site/
.. _`pep381client`: http://pypi.python.org/pypi/pep381client
.. _`z3c.pypimirror`: http://www.zopyx.com/blog/creating-a-local-pypi-mirror
.. _`SimpleHTTPServer`: http://docs.python.org/library/simplehttpserver.html
