MySQL, mysqldump et PHP : convertir de latin1 vers utf8
#######################################################
:date: 2010-03-08 07:38
:category: misc
:tags: mysql, php

Cet article à pour but de vous éviter, à vous lecteur, de vivre la perte
de neurones (et le gain de cheveux blancs) que j'ai subit dernièrement,
à investiguer des soucis de charset dans une base de donnée MySQL (et
l'affichage sur une page web par le biais de PHP).

Je tiens à préciser que je ne suis pas un expert MySQL, et encore moins
un expert en encoding, et certaines définitions ou mots utilisés dans
cet article peuvent ne pas être utilisés à bon escient. Le fond et la
méthode présentée ont par contre été vérifiés et testés!

Introduction à l'encoding
~~~~~~~~~~~~~~~~~~~~~~~~~

Je ne parlerais pas ici de ASCII ou Unicode (normes utilisées pour
stocker les données), mais du jeu de caractères utilisé pour *encoder*
ces données (et les afficher de manière lisible pour un être humain).
Pour commencer, quelques définitions:

#. `encoding`_ = character set = charset : jeu de caractères utilisé
   pour représenter des données
#. `utf8`_ = UTF-8 : un encoding qui associe un caractère à chaque
   "codepoint" `Unicode`_ (particularité: tous les caractères hors
   *latin1* sont stockés sur deux octets)
#. `latin1`_ = latin-1 = ISO-8859-1 : un encoding qui associe un
   caractère à chaque octet de la table `ASCII`_

Pour résumer, chaque caractère peut être stocké sur le disque en
Unicode (ou en ASCII, beaucoup plus limité). Il est ensuite *encodé*
(traduit, représenté) avec un jeu de caractères pour être affichable et
lisible par un être humain.

Historiquement, pour les pays occidentaux, l'encodage était fait en
latin1 (caractères latins avec ses accentuations). De nos jours, de plus
en plus d'applications se tournent vers Unicode et l'encodage en UTF-8
qui permet de représenter l'ensemble des caractères utilisés
universellement (il n'est donc pas limité aux caractères latins, mais
inclut par exemple les caractères cyrilliques, chinois...).

Charset utilisé par les tables et les champs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour consulter l'encodage utilisé par défaut pour une table ou un champ
particulier :

::

    mysql> SHOW CREATE TABLE bar;
    +-------+-------------------------------+
    | Table | Create Table                  |
    +-------+-------------------------------+
    | bar   | CREATE TABLE `bar` (
      `id` int(11) default NULL,
      `firstname` char(20) default NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=latin1 |
    +-------+-------------------------------+
    1 row in set (0.00 sec)

**ATTENTION :** les charset définits au niveau de la base de donnée, de
la table et du champ sont des "default charset". Il est tout à fait
possible d'avoir une table avec un champ dont le contenu est en
*latin1*, puis changer le *DEFAULT CHARACTER SET* à *utf8* pour ce
champ. Toutes les données existantes seront toujours en *latin1*, par
contre toutes les nouvelles données entrées en *utf8* seront en *utf8*.
On est alors confronté au pire des problèmes : des charsets différents
au sein d'une table pour un même champ.

Charset utilisé par le serveur, la database, les tables, les champs, le client, la connexion, les résultats...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les encodages utilisés par le client, la connexion, le serveur, et
l'affichage des résultats sont consultable par la commande suivante:

::

    mysql> SHOW VARIABLES WHERE variable_name like 'char%';
    +--------------------------+----------------------------+
    | Variable_name            | Value                      |
    +--------------------------+----------------------------+
    | character_set_client     | utf8                       |
    | character_set_connection | utf8                       |
    | character_set_database   | utf8                       |
    | character_set_filesystem | binary                     |
    | character_set_results    | utf8                       |
    | character_set_server     | latin1                     |
    | character_set_system     | utf8                       |
    | character_sets_dir       | /usr/share/mysql/charsets/ |
    +--------------------------+----------------------------+
    8 rows in set (0.00 sec)

Dans cet exemple, le client, la connexion, la database et les résultats
sont tous en *utf8*. Il n'y a que le serveur lui-même qui est en
*latin1* par défaut. Pour configurer le client, la connexion et les
résultats, on peut soit utiliser la commande

::

    mysql> SET NAMES utf8;

Soit configurer les variables décrites dans le paragraphe suivant :

Les variables de configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Elles peuvent être définies au niveau du fichier */etc/mysql/my.cnf*
(peut être situé à un autre endroit selon la distribution):

::

    [mysqld]
    default-character-set=utf8
    character-set-server=utf8
    collation-server=utf8_general_ci # utilisé pour les comparaisons

    [mysqldump]
    default-character-set=utf8

    [mysql]
    default-character-set=utf8

L'encoding du terminal: attention au piège!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quels que soit les charsets (par défaut) que vous avez configurés, il
faut savoir que c'est le charset du terminal (si vous êtes en ligne de
commande sur *mysql* par exemple) qui sera utilisé lors d'un *UPDATE* ou
*INSERT* dans une table.

Ainsi, même si vous avez tout configuré (y compris le *SET NAMES)* pour
être en *latin1*, lors d'une insertion dans une table, si votre terminal
est en *utf8* la donnée sera stockée en *utf8*.

Reportez-vous à `cette astuce`_ pour tester le charset (*latin1* ou
*utf8*) de votre terminal. Il faut **ABSOLUMENT que votre client ai le
même encoding que votre terminal pour éviter les `conflits`_ (à partir
de la page 21).**

Détecter le charset utilisé pour un champ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Commençons par une astuce pour différencier une donnée stockée en
*utf8* de *latin1 :*

::

    mysql> select firstname, length(firstname) from bar;
    +-----------+-------------------+
    | firstname | length(firstname) |
    +-----------+-------------------+
    | dédé    |                 6 |
    +-----------+-------------------+
    1 row in set (0.00 sec)

6 octets pour stocker 4 caractères ? C'est de l'*utf8*! Les accents
sont stockés sur deux octets. Si ça avait été du *latin1*, la longueur
de la donnée aurait été de 4 octets.

Mais alors, je peux demander à MySQL de convertir mes données ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Oui, mais pour savoir où aller, il faut savoir d'où on vient: avant de
demander à MySQL de convertir une donnée, il faut connaitre son encodage
actuel, et surtout dans quel encodage MySQL croit que ces données sont.

Il faut bien garder en tête que lorsqu'on parle du charset d'une table,
d'un champ, d'une base de donnée... on parle du charset par défaut, et
donc du charset que le serveur va utiliser pour insérer/retourner des
données. Cela n'a aucune incidence sur l'encodage utilisé auparavant
pour les données.

-  charset du serveur égal au charset du client : aucune conversion
   n'est faite
-  charset du serveur en *latin1*, charset du client en *utf8* : la
   donnée va être encodée en *utf8* (même si elle l'était déjà =>
   problème de double encoding)
-  charset du serveur en *utf8*, charset du client en *latin1* : la
   donnée va être encodée en *latin1*

Mes données sont stockées en *utf8* et MySQL ne le sait pas!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symptôme: quand on affiche le *length* d'une donnée avec des caractères
accentués, ça donne un nombre d'octets plus grands que le nombre de
caractères. La donnée est donc en *utf8*. Par contre, le serveur, la db,
la table, le champ... sont configurés pour être en *latin1*. Et quand on
essaie de faire un *SET NAMES utf8*, la donnée s'affiche avec des "Ã©" :
dans ce cas, c'est une donnée stockée en *utf8*, mais qui est
interprétée comme du *latin1* par MySQL, qui va donc l'encoder une
seconde fois en *utf8* (problème de double encoding).

La solution :
^^^^^^^^^^^^^

Le serveur pense que les données sont en *latin1* et on sait qu'elles
sont en *utf8* (notre charset final souhaité). Il suffit de

#. faire un dump de la base dans un fichier en *latin1* pour qu'il n'y
   ai aucune conversion (pas de double encoding)
#. modifier ce fichier pour y faire disparaitre toute trace de "latin1"
#. configurer la table, la base de donnée et le serveur pour qu'ils
   soient en "default charset *utf8*" (cf le chapitre sur les variables
   de configuration)
#. réimporter les données dedans

Mes données sont stockées en *latin1* et MySQL le sait, mais je les veux en *utf8*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vu que le serveur sait que ses données sont en *latin1*, il suffit de
lui demander de nous les fournir en *utf8* :

#. faire un dump de la base dans un fichier en *utf8* pour qu'il y ai
   une conversion automatique à partir de *latin1*
#. modifier ce fichier pour y faire disparaitre toute trace de "latin1"
#. configurer la table, la base de donnée et le serveur pour qu'ils
   soient en "default charset utf8" (cf le chapitre sur les variables de
   configuration)
#. réimporter les données dedans

Et PHP dans tout ça? Avant ça marchait, maintenant j'ai des � !
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ce cher PHP (hint: passez à `Django`_! c'est bien plus beau!) ne prends
pas en compte les configurations mises au niveau du serveur (ou du
fichier de configuration) pour son encoding!

Par défaut la commande *mysql\_connect* va toujours utiliser le charset
*latin1* : vous pouvez en avoir la preuve avec la commande
*mysql\_client\_encoding*.

PHP va donc vous fournir des données interprétées en *latin1* alors
qu'elles sont en *utf8*, d'où les caractères � non valides.

Il suffit alors d'utiliser la commande *mysql\_set\_charset('utf8', $connection)* sur la connexion ouverte avec *mysql\_connect*.

Faites bien attention d'avoir définit *utf8* pour l'encoding de vos
pages HTML soit par une balise *meta* dans votre entête de page, ou en
ayant configuré votre serveur web pour servir les pages en *utf8*. Un
moyen simple de vérifier ça est d'afficher les informations de la page.

.. _encoding: http://fr.wikipedia.org/wiki/Charset
.. _utf8: http://fr.wikipedia.org/wiki/Utf8
.. _Unicode: http://fr.wikipedia.org/wiki/Unicode
.. _latin1: http://fr.wikipedia.org/wiki/Latin1
.. _ASCII: http://fr.wikipedia.org/wiki/American_Standard_Code_for_Information_Interchange
.. _cette astuce: http://www.tuteurs.ens.fr/faq/utf8.html#test
.. _conflits: http://forge.mysql.com/w/images/b/b6/How_to_Use_Charsets_and_Collations_Properly.pdf
.. _Django: http://www.djangoproject.com/
