Checklist: différences entre MySQL et les modèles Django
########################################################
:date: 2009-03-02 10:54
:category: django

Comme vu dans un précédent billet (`MySQL et les modèles Django`_), il
existe des inconsistances entre une base de donnée MySQL et sa
représentation par des modèles Django.

Création des tables à partir des modèles Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lorsqu'on utilise *python manage.py syncdb*, les tables créées dans la
base de données

#. N'auront aucun commentaire, que ce soit sur les champs ou les tables,
   qu'il y ai ou non des *help\_text* et des *docstrings*
#. N'auront aucun champ `*ENUM*`_: les champs possédant une `liste de
   choix`_ sont représentés par un `*VARCHAR*`_ de longueur égale à la
   taille du plus long des choix
#. Les valeurs par défaut indiquées dans les modèles ne sont pas
   transmises dans les scripts de création des tables
#. Les `*BooleanField*`_ sont représentés par des `TINYINT`_ de 1bit
#. Un *DateTimeField* avec le paramètre *auto\_add\_now* ne sera pas
   représenté par un *TIMESTAMP* avec la valeur par défaut
   *CURRENT\_TIMESTAMP*

Inspection des tables dans Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Par ailleurs, si la base de donnée existe déjà, et que les modèles sont
créés automatiquement par l'utilisation de la commande *python manage.py
inspectdb*, il faudra garder à l'esprit que:

#. Les commentaires sur les champs et tables ne sont pas traduits en
   *help\_text* ou *docstrings*, il faudra donc les dupliquer
   manuellement
#. Un champ *ENUM* sera représenté par un *CharField*
#. Les tailles de champ ne sont pas respectées. Par exemple, un
   *Charfield* sera avec un *max\_length* de 135 par défaut
#. Les champs *TIMESTAMP* avec une valeur par défaut de
   *CURRENT\_TIMESTAMP* ne seront pas importés en champ avec une valeur
   par défaut *auto\_add\_now*
#. Les valeurs par défaut ne sont pas importées

Il y a deux derniers points à noter:

#. Le script d'inspection va importer les champs *primary\_key* pour
   chaque table, alors qu'ils peuvent être automatiquement générés de
   manière transparente: un modèle sans *primary\_key* explicite en aura
   un de manière implicite
#. Le script d'inspection va créer un modèle pour les tables utilisées
   pour les relations *ManyToMany* alors que là aussi, Django peut les
   générer de manière implicite dans la plupart des cas (lorsque cette
   table ne contient pas d'`information supplémentaire`_)

Je trouve préférable de laisser la gestion implicite des *primary\_key*
et des tables *ManyToMany* quand c'est possible, dans un soucis de
concision et de lisibilité.

Néanmoins, celà introduit une inconsistance entre les modèles et leur
représentation dans la base de donnée, inconsistance qui peut porter à
confusion.

Plus de cohérence entre les modèles et la base de donnée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Plusieurs possibilités:

- créer un script python qui va introspecter les modèles, et
  automatiquement rajouter les *help\_text* comme commentaires aux
  champs, et les *docstrings* comme commentaires aux tables, ou
  vice-versa
- Utiliser des `*Custom SQL*`_
- Créer des `*Custom fields*`_
- Pour le type *ENUM*, il existe un `*django snippet*`_ qui vise à
  apporter une meilleure cohérence dans son utilisation

Partagez vos astuces et faites part d'autres incohérences dans les
commentaires!

.. _MySQL et les modèles Django: ./mysql-et-les-modeles-django.html
.. _*ENUM*: http://dev.mysql.com/doc/refman/5.0/en/enum.html
.. _liste de choix: http://docs.djangoproject.com/en/dev/ref/models/fields/#choices
.. _*VARCHAR*: http://dev.mysql.com/doc/refman/5.0/en/char.html
.. _*BooleanField*: http://docs.djangoproject.com/en/dev/ref/models/fields/#booleanfield
.. _TINYINT: http://dev.mysql.com/doc/refman/4.1/en/numeric-types.html
.. _information supplémentaire: http://docs.djangoproject.com/en/dev/topics/db/models/#intermediary-manytomany
.. _*Custom SQL*: http://www.djangoproject.com/documentation/model-api/#database-backend-specific-sql-data
.. _*Custom fields*: http://docs.djangoproject.com/en/dev/howto/custom-model-fields/#howto-custom-model-fields
.. _*django snippet*: http://www.djangosnippets.org/snippets/864/
