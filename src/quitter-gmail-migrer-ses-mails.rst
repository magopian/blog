Quitter Gmail : migrer ses mails
################################
:date: 2013-08-05 19:07
:category: misc


Cet article est le quatrième d'une série sur comment reprendre le contrôle sur
son mail, et quitter son fournisseur de mail centralisé.

#. `Pourquoi quitter Gmail`_
#. `Réserver son propre nom de domaine`_
#. `Créer son compte mail`_
#. Migrer ses mails
#. `Gestion des contacts`_

.. _Pourquoi quitter Gmail: |filename|./quitter-gmail.rst
.. _Réserver son propre nom de domaine:
    |filename|./quitter-gmail-reserver-son-nom-de-domaine.rst
.. _Créer son compte mail: |filename|./quitter-gmail-creer-son-compte-mail.rst
.. _Gestion des contacts: |filename|./quitter-gmail-gestion-des-contacts.rst

Pour la plupart des gens, les mails sont stockés sur un serveur de mail, sur
une machine chez l'hébergeur.

Changer d'hébergeur revient donc à perdre tous ses mails, à moins de les avoir
au préalable tous sauvegardés.

Nous avons vu comment créer son compte mail, mais n'avons pas encore parlé de
la migration des mails vers ce nouvel hébergeur, nécessaire à la stratégie
courageuse de l'article précédent.

Commençons par quelques définitions.


Termes et définitions
=====================

IMAP
----

Le protocole
:abbr:`IMAP (Internet Message Access Protocol : protocole d'accès aux messages internet)`
permet de consulter ses mails, tout en les laissant sur le serveur, chez
l'hébergeur.

L'avantage est double : pour commencer, le message n'est téléchargé qu'au
moment de la visualisation, économisant de la bande passante et de l'espace
disque (imaginez la réception d'un mail énorme sur un téléphone portable à
l'espace limité).

Ensuite, vu que les messages restent sur le serveur, ils sont visualisables
depuis n'importe quel appareil à tout moment.

L'inconvénient étant que les messages, stockés sur le serveur, doivent être
migrés lors d'un changement d'hébergeur.


Comment
=======

Pour migrer ses mails, Jean va devoir commencer par rapatrier tous ses mails
sur son ordinateur. Et pour ça, il va être obligé d'utiliser un client lourd
(cf l'article précédent).

Nous allons prendre l'exemple de Thunderbird.


Connecter Thunderbird à Gmail
-----------------------------

C'est la partie la plus simple : il suffit de `créer un nouveau compte`_.

.. _créer un nouveau compte:
    https://support.mozillamessaging.com/fr/kb/configuration-automatique-de-compte


Configurer la synchronisation
-----------------------------

Il faut ensuite être sûr que le compte nouvellement créé est configuré pour que
tous les messages soient conservés sur l'ordinateur.

Pour cela, cocher la case « Conserver les messages de ce compte sur cet
ordinateur », comme indiqué sur la page d'aide `configurer la synchronisation
et l'espace disque`_.

.. _configurer la synchronisation et l'espace disque:
    https://support.mozillamessaging.com/fr/kb/le-protocole-imap#w_configurer-la-synchronisation-et-laoespace-disque


Rapatrier les mails
-------------------

Il ne reste plus qu'à passer Thunderbird en mode « hors ligne », pour forcer la
synchronisation, ce qui dans notre cas correspond au téléchargement de tous les
mails de Gmail.

Le passage en mode hors ligne se fait en cliquant sur la petite icône, tout en
bas à gauche de la fenêtre de Thunderbird, dans la barre de statut, ou par le
menu ``Fichier » Hors Ligne » Travailler hors ligne``.

Selon le nombre de mails, et leur taille, cela peut prendre un long moment.
Pour information, il a fallut pas loin d'une heure pour télécharger un peu plus
de 5000 mails, pour une taille totale de 2,23Go, avec une bonne connexion
internet.


Transférer sur le nouvel hébergeur
----------------------------------

Maintenant que tous les messages sont téléchargés, il ne reste plus qu'à faire
un gros copier-coller de tous les messages du compte Gmail vers le compte sur
le nouvel hébergeur.

Attention, cette manipulation prendra beaucoup plus longtemps que le
téléchargement des mails. En effet, les connexions internet de nos jours sont
assymétriques : on télécharge beaucoup plus vite qu'on envoie.

Une fois l'envoi de tous les mails terminés, ils seront accessibles directement
par le biais du nouveau compte créé à l'article précédent, celui sur le nouvel
hébergeur.


La suite
========

Si Jean utilise Thunderbird au quotidien, il aura tous ses mails synchronisés
entre l'hébergeur et son ordinateur, et donc :

* une copie de ses mails sur l'hébergeur
* une copie de ses mails sur son ordinateur
* une copie de ses mails sauvegardés par ses soins
* une étape de moins à exécuter (le rapatriement) lors du prochain changement
  d'hébergeur
* la possibilité de travailler hors ligne

.. note:: Vous DEVEZ avoir une sauvegarde de tous vos fichiers, pas seulement
    de vos mails !

Le prochain article abordera la Gestion des contacts.
