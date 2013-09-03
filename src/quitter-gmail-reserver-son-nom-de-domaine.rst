Quitter Gmail : réserver son nom de domaine
###########################################
:date: 2013-07-30 13:44
:category: misc
:status: draft


Cet article est le deuxième d'une série sur comment reprendre le contrôle sur
son mail, et quitter son fournisseur de mail centralisé.

#. `Pourquoi quitter Gmail`_
#. Réserver son propre nom de domaine
#. `Créer son compte mail`_
#. `Migrer ses mails`_
#. `Gestion des contacts`_

.. _Pourquoi quitter Gmail: |filename|./quitter-gmail.rst
.. _Créer son compte mail: |filename|./quitter-gmail-creer-son-compte-mail.rst
.. _Migrer ses mails: |filename|./quitter-gmail-migrer-ses-mails.rst
.. _Gestion des contacts: |filename|./quitter-gmail-gestion-des-contacts.rst

Nous allons voir dans un prochain article comment créer son compte mail, mais
cela nécessite d'avoir au préalable son propre nom de domaine.

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


Nom de domaine
--------------

On peut voir les noms de domaine comme une entrée dans un annuaire, qui fait
correspondre un nom à un numéro de téléphone ou une adresse.

Un nom de domaine s'achète auprès d'un
:abbr:`registrar (Organisme chargé de l'attribution de noms de domaines)`
(comme BookMyName_ par exemple) ou d'un intermédiaire, comme un hébergeur qui
s'en occupe pour vous.

.. _BookMyName: http://bookmyname.com

Selon les extensions (la dernière partie d'un nom de domaine, comme par exemple
*.fr* pour *dupont.fr*), et selon le *registrar* ou l'intermédiaire, un nom de
domaine coûtera entre 5€ et 15€ par an en moyenne.


Comment
=======

Passer directement par un *registrar* est moins cher mais nécessite une
configuration par le biais de son interface d'administration pour indiquer qui
(quel serveur) va s'occuper techniquement de vos emails.

L'intérêt de passer par le biais d'un hébergeur est qu'il n'y a pas besoin de
se soucier de cette configuration, et que la gestion centralisée de ce nom de
domaine et du compte mail est plus pratique.

Dans tous les cas, le nom de domaine acheté vous est réservé, et vous le faites
pointer vers où vous voulez tant qu'il vous est réservé. Vous pouvez par
ailleurs décider de transférer la gestion de ce nom de domaine à un autre si
vous le souhaitez : Par exemple, Jean peut avoir acheté son domaine chez
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
enregistrements suivants, spécifiques à la gestion des mails (pour un
hébergement de site web ce sera différent) :

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
nom de domaine pour pointer vers son nouvel hébergeur, vers son nouveau compte
mail... Et cela sans impacter qui que ce soit.

Le prochain article expliquera comment `Créer son compte mail`_.


.. note:: Je n'ai aucun intéressement chez Alwaysdata_ ni chez BookMyName_, si
          je les prend en exemple c'est que je suis (ou ai été, dans le cas de
          BookMyName) un client satisfait.
