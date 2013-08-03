Quitter Gmail : réserver son nom de domaine
###########################################
:date: 2013-07-30 13:44
:category: misc
:status: draft


Cet article est le deuxième d'une série sur `quitter gmail`_.

.. _quitter gmail: |filename|./quitter-gmail.rst

Nous allons voir dans un prochain article comment reprendre le contrôle sur son
adresse mail (`Créer son compte mail`_), mais cela nécessite d'avoir au
préalable son propre nom de domaine.

.. _Créer son compte mail:
    |filename|./quitter-gmail-creer-son-compte-mail.rst

Commençons par quelques définitions.


Termes et définitions
=====================

Hébergeur
---------

Un hébergeur s'occupe d'une machine pour vous. Pour qu'une machine (un serveur)
soit accessible à d'autres, pour qu'ils puissent aller sur votre site internet,
vous envoyer un mail... il faut que cette machine soit :

* correctement configurée
* toujours allumée
* administrée au quotidien : mises à jour de sécurité, installation de
  nouvelles version...

Vous pouvez tout à fait vous en occuper vous-même, si vous en avez les
compétences, les ressources et le temps nécessaire à y consacrer. Pour la
plupart des gens, ce n'est pas le cas, et un hébergeur le fait pour vous.

Un hébergeur va donc vous louer une machine (ou une partie de cette machine),
avec différents services :

* hébergement de site internet
* base de données
* stockage de fichiers
* compte mail (c'est ce qui nous intéresse plus particulièrement dans le cadre
  de cette série d'articles)

Certains proposent des packs, comme par exemple Alwaysdata_ qui propose pour
moins de 10€ par mois autant de comptes mails qu'on le souhaite, des bases de
données, du stockage de fichiers, de l'hébergement de site web...

.. _AlwaysData: https://alwaysdata.com


Registrar
---------

Un registrar est un organisme qui est chargé d'attribuer des noms de domaine,
de les louer, de les réserver pendant une certaine durée à ses clients.

Ainsi, Jean Dupont peut s'adresser à un registrar comme BookMyName_ pour
réserver son nom de domaine *dupont.fr*.

.. _BookMyName: http://bookmyname.com


Nom de domaine
--------------

On peut voir les noms de domaine comme une entrée dans un annuaire, qui fait
correspondre un nom à un numéro de téléphone ou une adresse.

Dans notre cas, ils permettent de faire une correspondance entre un nom et un
serveur (une machine, quelque part sur internet). Les serveurs ont des
adresses :abbr:`IP (Internet Protocol)`, qui sont composées d'une série de
chiffres (et éventuellement de lettres).

Ces adresses IP sont très pratiques pour aiguiller et acheminer les messages,
quels qu'ils soient, sur internet, car les machines savent très bien les
utiliser. Pour nous autres humains, en revanche, il est moins aisé de retenir
*127.0.0.1* ou encore *ba27:ebff:feff:8e68*.

Un service permet de pallier à ce problème : la résolution de noms de domaine,
par le biais de :abbr:`DNS (Domain Name Server : Serveur de noms de domaine)`.
Il fait correspondre un nom humainement reconnaissable et plus facile à retenir
(par exemple *dupont.fr*) à une adresse IP.

Un nom de domaine peut être configuré pour correspondre à une adresse IP
différente lorsque c'est nécessaire, permettant de changer de serveur (ou
d'hébergeur) sans que les utilisateurs aient à s'en soucier.

Un nom de domaine se loue. On dit qu'on réserve un nom de domaine, pour une
durée déterminée, et on paie pour cette durée. Au bout de cette durée, il faut
reconduire la réservation, ou le nom de domaine pourra être attribué à
quelqu'un d'autre.

Selon les extensions (la dernière partie d'un nom de domaine, comme par exemple
*.fr* pour *dupont.fr*), et selon le *registrar* ou l'intermédiaire
(revendeur), un nom de domaine coûtera entre 5€ et 15€ par an en moyenne.


Enregistrement CNAME
--------------------

Il est possible d'ajouter plusieurs types d'enregistrement sur un nom de
domaine. Un de ces type d'enregistrements est le *CNAME*, raccourci pour
*canonical name*.

Ce type d'enregistrement permet de déclarer un alias, par exemple que
*dupont.fr* est un équivalent au nom de domaine fourni par votre hébergeur.

C'est une des manières de faire pointer un nom de domaine vers un serveur
spécifique.


Enregistrement MX
-----------------

Il existe un enregistrement particulier, appelé
:abbr:`MX (Mail eXchange)`, spécifique aux serveurs de mails. Ainsi, Jean peut
configurer un enregistrement MX sur son nom de domaine *dupont.fr* pour que
tous les mails envoyés à *@dupont.fr* soient envoyés (puis traités) par le
serveur mail (l'hébergeur) de son choix.

Cette manipulation n'est pas nécessaire si vous louez votre nom de
domaine sur le même hébergeur qui vous fournit un compte mail : c'est souvent
automatique.


Comment
=======

Pour réserver un nom de domaine, il faut soit faire appel à un *registrar*,
soit à un intermédiaire comme votre hébergeur.

Passer directement par un *registrar* est moins cher, et nécessite une
configuration par le biais de son interface d'administration, des
enregistrements souhaités (par exemple *CNAME* et *MX*).

L'intérêt de passer par le biais d'un hébergeur est qu'il n'y a pas besoin de
se soucier de cette configuration, et que la gestion centralisée de ce nom de
domaine et du compte mail ou web est plus pratique.

Dans tous les cas, le nom de domaine vous est réservé, et vous le faites
pointer vers où vous voulez tant qu'il vous est réservé. Vous pouvez par
ailleurs décider de dédier la gestion de ce nom de domaine à un autre si vous
le souhaitez : Par exemple, Jean peut avoir acheté son domaine chez
BookMyName_ (registrar), et l'avoir transféré par la suite chez Alwaysdata_
(hébergeur).


Trouver un nom de domaine
-------------------------

La plupart des *registrar* et des intermédiaires mettent à disposition un outil
de recherche sur le nom de domaine et son extension.

Ainsi, Jean pourrait faire une recherche sur "dupont", et voir qu'il y a
plusieurs domaines libres :

* dupont.fr
* dupont.org
* dupont.net
* dupont.info
* dupont.com
* ou encore d'autres...

Il peut alors en choisir un, ou plusieurs si il le souhaite. Dans ce dernier
cas, il pourra décider de tous les faire pointer vers le même endroit.


Configurer un nom de domaine
----------------------------

Cette étape n'est nécessaire que lorsque le nom de domaine a été réservé par un
autre biais que l'hébergeur lui-même.

Voici l'exemple de Jean Dupont qui veut faire pointer son nom de domaine
*dupont.fr* acheté chez BookMyName vers son hébergeur Alwaysdata. Au niveau de
l'interface d'administration de BookMyName, il doit rajouter les
enregistrements suivants :

Pour le nom de domaine :

========= ===== === =====================
domain    Type  TTL Value
========= ===== === =====================
dupont.fr CNAME   5 dupont.alwaysdata.net
========= ===== === =====================

.. note:: la valeur indiquée correspond au compte créé par Jean Dupont

Pour la réception de mails :

========= ==== === ======== ==================
domain    Type TTL Priority Value
========= ==== === ======== ==================
dupont.fr MX   5   10       mx1.alwaysdata.com
dupont.fr MX   5   20       mx2.alwaysdata.com
========= ==== === ======== ==================

Il faut ensuite se connecter à son compte Alwaysdata, `rajouter le nom de
domaine`_, et créer son adresse mail (par exemple *jean@dupont.fr*).

.. _rajouter le nom de domaine:
    http://wiki.alwaysdata.com/wiki/Ajouter_un_domaine


La suite
========

Et demain ? Si jamais Jean décide de changer d'hébergeur, de *registrar*, de
serveur de mail ?

Il n'aura plus aucun soucis : il lui suffira de changer la configuration de son
nom de domaine (en modifiant ses enregistrements *CNAME* et *MX* par exemple)
pour pointer vers son nouvel hébergeur, vers son nouveau compte mail... Et cela
sans impacter qui que ce soit.

Le prochain article expliquera comment `Créer son compte mail`_.


.. note:: Je n'ai aucun intéressement chez Alwaysdata_ ni chez BookMyName_, si
          je les prend en exemple c'est que je suis (ou ai été, dans le cas de
          BookMyName) un client satisfait.
