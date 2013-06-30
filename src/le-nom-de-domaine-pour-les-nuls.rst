Le nom de domaine pour les nuls
###############################
:date: 2013-06-30 09:50
:category: misc


Cet article est le deuxième d'une série sur les mails. Il est destiné aux
personnes n'ayant pas ou peu de connaissances techniques du domaine, et a pour
but de permettre à chacun de reprendre le contrôle sur son adresse mail.

Si vous ne l'avez pas déjà lu, vous pouvez vous reporter à l'article `Quitter
Gmail pour les nuls`_.

.. _Quitter Gmail pour les nuls: |filename|./quitter-gmail-pour-les-nuls.rst


Pourquoi
========

De nos jours, il est très facile de se passer de son identité numérique. Ou
plutôt, il est très difficile d'en garder le contrôle. Il devient monnaie
courante d'abandonner nos données aux services tiers comme Google ou Facebook.
On se construit alors son identité sur ces réseaux, sur ces "silos" à données.

Il ne faut pas se leurrer, ce ne sont alors plus nos données, notre identité,
tout leur appartient, et tout leur est utile à des fins commerciales. Ces
services vont ainsi pouvoir revendre vos données, ou s'en servir pour vous
présenter des publicités toujours plus ciblées.

Cela pose soucis lorsque ces tiers décident de clore un compte, d'en censurer
un, de fournir l'accès à toutes les données à la 
:abbr:`NSA (National Security Agency, les services secrets des États-Unis)`, de
diminuer la zone "privée", en fournissant toujours plus de vos informations aux
autres.

Un autre soucis : celui du contrôle sur les informations, photos, vidéos...
Choisir de ne plus donner accès à cette photographie désavantageuse prise lors
d'une soirée trop alcoolisée et qui pourrait nuire lors d'un entretien
d'embauche ?
Ou encore profiter soi-même des revenus de la publicité sur la génération de
son contenu, ou tout simplement le mettre à disposition entièrement
gratuitement (le contenu de ce blog).

Nous avons vu comment reprendre le contrôle sur son adresse mail dans l'article
`Quitter Gmail pour les nuls`_, mais cela nécessite d'avoir au préalable son
propre nom de domaine.

Nous allons donc maintenant voir comment réserver son nom de domaine.


Termes et définitions
=====================

Hébergeur
---------

Un hébergeur héberge une machine pour vous. Pour qu'une machine (un serveur)
soit accessible à d'autres, pour qu'ils puissent aller sur votre site internet,
vous envoyer un mail... il faut que cette machine soit :

* correctement configurée
* démarrée
* gérée au quotidien : mises à jour de sécurité, installation de nouvelles
  version, administration...

Vous pouvez tout à fait vous en occuper vous-même, si vous en avez les
compétences, les ressources et le temps nécessaire à y consacrer. Pour la
plupart des gens, ce n'est pas le cas, et un hébergeur le fait pour vous.

Un hébergeur va donc vous louer une machine (ou une partie de cette machine),
avec différents services :

* hébergement de site internet
* compte mail
* base de données
* stockage de fichiers

Certains proposent des packs, comme par exemple Alwaysdata_ qui propose pour
moins de 10€ par mois pour autant de comptes mails qu'on le souhaite, bases de
données, stockage de fichiers, hébergement de site web...

.. _AlwaysData: https://alwaysdata.com


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
utiliser. Pour les êtres humains, en revanche, il est moins aisé de retenir
*127.0.0.1* ou encore *ba27:ebff:feff:8e68*.

Un service permet de pallier à ce problème : la résolution de noms de domaine,
par le biais de :abbr:`DNS (Domain Name Server, Serveur de noms de domaine)`.
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
*.fr* pour *dupont.fr*), et selon le *registrar* ou l'intermédiaire, un nom de
domaine coûtera entre 5€ et 15€ par an en moyenne.


Enregistrement MX
-----------------

Il existe un enregistrement particulier, appelé
:abbr:`MX (Mail eXchange)`, spécifique aux serveurs de mails. Ainsi, Jean peut
configurer un enregistrement MX sur son nom de domaine *dupont.fr* pour que
tous les mails envoyés à *@dupont.fr* soient envoyés (puis traités) par le
serveur mail (l'hébergeur) de son choix.

Cette manipulation n'est généralement pas nécessaire si vous louez votre nom de
domaine sur le même hébergeur qui vous fournit un compte mail. En effet,
l'hébergeur peut vous associer automatiquement le nom de domaine (et
l'enregistrement MX) à ses propres serveurs, vous évitant d'avoir à le faire
manuellement.


Comment
=======

Pour réserver un nom de domaine, il faut soit faire appel à un *registrar* (un
organisme qui est chargé d'attribuer des noms de domaine), soit à un
intermédiaire comme votre hébergeur.

Il est tout à fait possible de réserver son nom de domaine directement chez un
*registrar* (souvent moins cher), et ensuite configurer son nom de domaine (en
général par le biais d'une interface d'administration fournie par ce
*registrar*) pour qu'il pointe sur l'adresse IP de votre machine, du serveur de
votre hébergeur, ou sur quoi que ce soit d'autre.

L'intérêt de passer directement par un hébergeur réside dans le fait qu'il n'y
a normalement pas besoin de ce soucier de cette configuration, et que la
gestion centralisée de ce nom de domaine et du compte mail ou web est plus
pratique.

Dans tous les cas, le nom de domaine vous appartient, et vous le faites pointer
vers où vous voulez tant qu'il vous est réservé. Vous pouvez même décider de
dédier la gestion de ce nom de domaine à un autre si vous le souhaitez.

Par exemple, Jean peut avoir acheté son domaine chez BookMyName_, et l'avoir
transféré par la suite chez Alwaysdata_.

.. _BookMyName: http://bookmyname.com


Trouver un nom de domaine
-------------------------

La plupart des *registrar* et des intermédiaires mettent à disposition un outil
de recherche simple sur le nom de domaine et son extension.

Ainsi, Jean pourrait faire une recherche sur "dupont", et voir qu'il y a
plusieurs possibilités :

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

Cette étape n'est généralement nécessaire que lorsque le nom de domaine a été
réservé par un autre biais que l'hébergeur lui-même.

TODO : Pointer vers une adresse IP (A, CNAME ...)
TODO : Pointer vers un serveur mail (MX)


Conclusion
==========

Et demain ? Si jamais Jean décide de changer d'hébergeur, de *registrar* de
serveur de mail ?

Il n'aura plus aucun soucis : il lui suffira changer la configuration de son
nom de domaine pour pointer vers son nouvel hébergeur, vers son nouveau compte
mail... Et cela sans impacter qui que ce soit.


.. note:: Je n'ai aucun intéressement chez Alwaysdata_, si je les prend en
          exemple c'est que je suis un client satisfait.
