MySQL et les modèles Django
###########################
:date: 2009-02-24 19:45
:category: django

Le problème
~~~~~~~~~~~

D'un côté, une base de donnée `MySQL`_ maintenue par `MySQLWorkbench`_.
De l'autre, `Django`_ et ses modèles.

Entre les deux... pas grand chose.

Les acquis
~~~~~~~~~~

MySQL et MySQLWorkbench
^^^^^^^^^^^^^^^^^^^^^^^

MySQLWorkbench est un outil excellent pour pouvoir maintenir une base
de donnée:

#. Gestion des commentaires sur les tables et champs
#. Affichage des relations entre les tables d'une base de données sous
   forme d'un schéma
#. Facilité de modification d'une base de donnée en production par
   l'export de scripts SQL

Django et les modèles
^^^^^^^^^^^^^^^^^^^^^

Django, de son côté, nécéssite une représentation de la base de donnée
par des modèles. Ces modèles sont des classes codées en Python:

#. Facilité de suivi des modifications d'un modèle par le biais d'un
   contrôle de version (Git, Mercurial, SVN ...) accompagné de
   commentaires pour chaque *commit*
#. Facilité de documentation: un paramètre *help\_text* pour chaque
   champ, un *docstring* pour chaque modèle
#. Abstraction de certaines tables et champs générés automatiquement
   (comme les *primary key* ou les tables *ManyToMany*)

Les outils
~~~~~~~~~~

Comme indiqué plus haut, MySQLWorkbench permet d'exporter des scripts
SQL de création et/ou de modification. Il est aussi possible de *reverse
engineer* le dump SQL d'une base de donnée, et ainsi créer toutes les
tables dans l'interface graphique, et y visualiser les relations sous
forme de schéma.

Django permet l'export de scripts SQL de création, mais aussi
l'inspection d'une base de données (par la commande *python manage.py
inspectdb*), ou encore l'exécution de scripts SQL *custom* à chaque
création/modification d'une table (par la commande *python manage.py
syncdb*).

Les méthodes
~~~~~~~~~~~~

La méthode basique
^^^^^^^^^^^^^^^^^^

... qui casse complètement le principe *DRY* (Don't Repeat Yourself):
maintenir les deux parties en parallèle.

Lorsqu'il faut rajouter une table dans la base, ou y apporter une
modification, faire la modification dans MySQLWorkbench, puis répliquer
l'ajout/la modification dans les modèles Django.

Pour: Méthode simple, pas de procédure ou méthode à mettre en place.

Contre: Méthode manuelle, sujette à l'erreur humaine (faute de typo,
oubli...).

MySQLWorkbench => Django
^^^^^^^^^^^^^^^^^^^^^^^^

#. Maintenance dans l'outil MySQLWorkbench, puis export des scripts de
   création/modification.
#. Execution de ce script sur la base de données pour la mettre à jour
#. Utilisation de *inspectdb* avec Django pour mettre à jour les modèles

Pour: Méthode automatique, donc pas de risque de typo ou d'oubli

Contre: Méthode très complexe à mettre en place. En effet, *inspectdb*
est loin de créer des modèles fidèles, et il manque de nombreuses
informations (un futur billet sera écrit sur ce sujet).

Django => MySQLWorkbench
^^^^^^^^^^^^^^^^^^^^^^^^

#. Ajout ou modification d'un modèle dans Django
#. Mise à jour de la base de donnée en utilisant *python manage.py
   syncdb* (et des scripts *custom* si nécéssaire)
#. Utilisation de MySQLWorkbench pour *reverse engineer* les scripts de
   création de la base de donnée

Pour: Méthode automatique, donc pas de risque de typo ou d'oubli. De
plus, contrairement à la méthode précédente, la représentation des
tables est 100% fidèle à la structure de la base de donnée créée par les
Django.

Contre: Toutes les informations de commentaires (et d'autres, comme
nous le verrons dans un futur billet) sont perdues à chaque
modification.

Conclusion
~~~~~~~~~~

Je n'ai malheureusement pas trouvé à l'heure actuelle de méthode
miracle. Il y a `des pistes`_, mais il semble qu'il n'y ai rien de
concret pour le moment.

Pour certains cas particuliers, l'une ou l'autre méthode sera préférée:

#. Création d'une nouvelle table: la méthode Django => MySQLWorkbench
   sera facile à mettre en place, et il n'y aura rien de perdu vu qu'il
   n'y a pas d'existant
#. Modification d'une table par le rajout d'un nouveau champ: l'une des
   deux méthodes automatique peuvent faire l'affaire
#. Modification d'un champ d'une table: la méthode manuelle sera en
   général la plus rapide et la plus simple à mettre en place
#. Modifications complexes, multiples, perte de donnée possible...: dans
   ce cas, point de salut, il ne reste que la méthode manuelle, et une
   grande concentration!

Et vous, quelle est votre méthode?

.. _MySQL: http://www.mysql.com/
.. _MySQLWorkbench: http://dev.mysql.com/downloads/workbench/5.1.html
.. _Django: http://www.djangoproject.com
.. _des pistes: http://code.djangoproject.com/wiki/SchemaEvolution
