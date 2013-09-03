Quitter Gmail : créer son compte mail
#####################################
:date: 2013-06-25 08:34
:category: misc
:status: draft


Cet article est le troisième d'une série sur comment reprendre le contrôle sur
son mail, et quitter son fournisseur de mail centralisé.

#. `Pourquoi quitter Gmail`_
#. `Réserver son propre nom de domaine`_
#. Créer son compte mail
#. `Migrer ses mails`_
#. `Gestion des contacts`_

.. _Pourquoi quitter Gmail: |filename|./quitter-gmail.rst
.. _Réserver son propre nom de domaine:
    |filename|./quitter-gmail-reserver-son-nom-de-domaine.rst
.. _Migrer ses mails: |filename|./quitter-gmail-migrer-ses-mails.rst
.. _Gestion des contacts: |filename|./quitter-gmail-gestion-des-contacts.rst

Dans cet article nous allons étudier les différentes possibilités et stratégies
pour se passer de Gmail pour son adresse mail.

Pour rappel, Jean Dupont, qui utilisait jusqu'à présent son adresse
*jean.dupont@gmail.com*, vient de se procurer un compte mail chez son
hébergeur, ainsi qu'un nom de domaine et une adresse *jean@dupont.fr* qui
pointent vers cet hébergeur.

Commençons par quelques définitions.


Termes et définitions
=====================

Adresse mail
------------

C'est l'équivalent du numéro de téléphone. C'est ce qui permet d'acheminer les
messages au bon endroit.

Il faut donc voir l'adresse mail comme une localisation qui peut changer (le
même numéro pourrait être chez SFR un jour, et chez Bouygues le lendemain).

Une adresse email est composée de deux éléments :

* *jean* : la partie précédent le *@*, la partie variable, qui correspond au
  compte mail sur le serveur mail
* *dupont.fr* : la partie après le *@*, qui est le nom de domaine (se référer à
  l'article précédent), et qui pointe vers un serveur mail

Si Jean le souhaite, il peut modifier *dupont.fr* pour qu'il pointe sur un
autre serveur mail et y créer un nouveau compte, contrairement à l'adresse
*jean.dupont@gmail.com* qui appartient à Google, et qui ne pointera jamais
ailleurs que sur les serveurs de Google.


Compte mail
-----------

C'est l'équivalent de la boite postale dans lequel le facteur dépose votre
courrier. C'est l'endroit où arrivent tous les messages.

Contrairement à la boite postale qui ne sert que temporairement, le temps de
récupérer le courrier, un compte mail peut stocker les messages aussi longtemps
qu'on le souhaite.

Ce compte est localisé sur un serveur, une machine. En reprenant l'exemple de
Gmail, le compte est localisé sur une machine « chez Google ».

À la manière d'un dossier sur un ordinateur, un compte stocke tous les messages
reçus, envoyés, supprimés, classés dans des sous-dossiers, déplacés dans les
spams...


Client mail
-----------

Le programme qui permet de :

* lister les messages
* lire les messages
* écrire des messages
* trier, ordonner, classer les messages

Accessoirement, un client permet aussi de gérer les adresses (contacts), mais
c'est un autre sujet que nous aborderons dans un futur article de cette série.

Il existe deux grands types de clients :

* le client web : un site, comme par exemple http://mail.google.com

  - s'utilise sur le port 80, qui est rarement bloqué (dans les hôtels, sur les
    accès wifi publics, dans les entreprises...)
  - ne nécessite pas d'installation de logiciel sur son ordinateur
  - ne nécessite pas de configuration (dans le cas où il est fourni directement
    par l'hébergeur du compte utilisé)

* le client lourd : un programme à installer sur son ordinateur, comme par
  exemple Thunderbird_

  - sauvegarde les messages sur l'ordinateur
  - plus pratique et ergonomique qu'un client web
  - peut être utilisé hors connexion : les messages à envoyer sont stockés puis
    envoyés lors de la prochaine connexion
  - n'est pas dépendant d'un hébergeur, et donc tous les mails seront conservés
    le jour d'un changement

.. _Thunderbird: http://www.mozilla.org/fr/thunderbird/?flang=fr

Dans une certaine limite, les clients sont interchangeables. Ainsi, on peut
utiliser le **client** Thunderbird pour accéder à un **compte** Gmail.


Redirection
-----------

Comme un renvoi d'appel ou le suivi de courrier postal : il permet de faire
suivre tout le courrier normalement destiné à une adresse vers une autre
adresse.

Ainsi, Jean peut décider de rediriger tous les messages destinés à
*jean@dupont.fr* vers l'adresse *jean.dupont@gmail.com*.


Sauvegarde
----------

Il est possible de conserver plusieurs copies de ses messages, afin d'avoir une
sauvegarde en cas de défaillance d'une machine (son ordinateur, la machine de
son hébergeur...).

Exemple : l'utilisation d'un client lourd comme Thunderbird permet d'avoir une
copie des messages sur son ordinateur, tout en les conservant sur le serveur
(sur le compte). On peut alors envisager de sauvegarder ces messages (qui sont
stockés sous forme de fichiers sur l'ordinateur) sur un disque USB, un
:abbr:`NAS (Network-Attached Storage : disque dur réseau)`...


Comment
=======

Jean veut avoir le contrôle de la destination de ses messages, afin de pouvoir
changer d'avis si il le souhaite. Il va donc faire passer le mot que sa
nouvelle adresse est désormais *jean@dupont.fr*, et non plus
*jean.dupont@gmail.com*.

Par contre, Jean veut toujours recevoir les mails envoyés à
*jean.dupont@gmail.com*, car il y a beaucoup d'entités qui ne connaissent pas
encore sa nouvelle adresse, comme les impôts, EDF, ou encore des abonnements à
des listes de diffusion...

Avant de rentrer dans le détail, voici les deux stratégies proposées :

* timorée : conserver Gmail comme compte principal
* courageuse : utiliser son nouveau compte comme compte principal

Ces deux étapes sont indépendantes, et il est tout à fait possible de rester à
la première étape, ou encore de passer directement à la deuxième étape.

Le plus important est de pouvoir utiliser sa nouvelle adresse mail, afin
d'avoir à minima le contrôle sur la destination des messages.


Stratégie timorée : Conserver Gmail comme compte principal
==========================================================

Cette stratégie est un compromis qui permet de ne pas changer grand chose à ses
habitudes quotidiennes, en continuant à utiliser le client Gmail.

L'inconvénient est que Google a toujours accès à tous les messages, et cette
stratégie demande plus de configuration.


Rediriger *jean@dupont.fr* vers *jean.dupont@gmail.com*
-------------------------------------------------------

C'est la toute première chose à faire. Sur son hébergeur, Jean va configurer
son adresse *jean@dupont.fr* pour qu'elle redirige tous les messages vers
*jean.dupont@gmail.com*.

Ainsi, dès que quelqu'un écrira à *jean@dupont.fr*, le message sera
automatiquement transféré, relayé, redirigé vers *jean.dupont@gmail.com* (comme
si il avait été destiné à *jean.dupont@gmail.com* dès le début).

Il accédera alors à ses messages toujours de la même manière, en se connectant
sur http://mail.google.com.

Cette redirection devra rester en place tant que la stratégie courageuse ne
sera pas mise en place.


Configurer le client Gmail : envoyer les mails de la part de *jean@dupont.fr*
-----------------------------------------------------------------------------

Par défaut, un client mail envoie tous les mails de la part de l'adresse mail
associée au compte sur lequel le client se connecte.

Ainsi, le client Gmail va automatiquement envoyer tous les mails de la part de
*jean.dupont@gmail.com*.

Prenons le scénario suivant :

* *bill@smith.com* envoie un mail à *jean@dupont.fr*
* le mail arrive sur l'hébergeur de Jean, qui redirige le message vers
  *jean.dupont@gmail.com*
* le mail arrive chez Google sur son compte
* Jean consulte le message et y répond
* le client Gmail envoie la réponse de la part de *jean.dupont@gmail.com*
* et là Bill répondra à l'adresse Gmail, au lieu de l'adresse *jean@dupont.fr*

Jean aura beau eu faire part de sa nouvelle adresse, dans les faits, la plupart
des messages continueront à être directement envoyés à son adresse Gmail.

Il lui faut donc configurer son client Gmail pour qu'il envoie tous les mails
de la part de *jean@dupont.fr*.

Il y a une page expliquant comment faire cela : `Envoi de message avec une
autre adresse`_.

.. _Envoi de message avec une autre adresse:
    https://support.google.com/mail/answer/22370?hl=fr&ctx=mail

Voici une explication résumée (si vous utilisez Alwaysdata, reportez-vous en
fin de cette article pour des captures d'écran explicatives) :

.. _AlwaysData: https://alwaysdata.com

#. Cliquez sur l'icône représentant une roue dentée en haut à droite de
   l'écran, puis sélectionnez Paramètres
#. Cliquez sur l'onglet Comptes
#. Sous « Envoyer des e-mails en tant que », cliquez sur « Ajouter une autre
   adresse e-mail »
#. Dans le champ « Adresse e-mail », saisissez votre nom (Jean Dupont) et
   l'autre adresse e-mail (*jean@dupont.fr*), et décochez la case « Traiter
   comme un alias »
#. Choisissez l'option « Utiliser les serveurs SMTP de votre autre fournisseur de messagerie »
#. Entrez les informations de connexion au compte de votre hébergeur
#. Cliquez sur « Enregistrer les modifications »
#. De retour dans les paramètres du compte, cliquez sur le lien « utiliser par
   défaut » à droite de la nouvelle adresse que vous venez de créer
#. Choisissez enfin, sous « En réponse à un message », l'option « Toujours
   répondre à partir de l'adresse par défaut (actuellement jean@dupont.fr) »

Suite à ce changement, tous les mails qui seront envoyés à partir du client
Gmail seront envoyés de la part de *jean@dupont.fr*, et donc toutes les
personnes qui répondent, répondront directement à cette nouvelle adresse mail.

Tous les mails envoyés à *jean@dupont.fr* ou à *jean.dupont@gmail.com*
arriverons sur son compte Gmail.


Stratégie courageuse : Utiliser son nouveau compte
==================================================

Bien qu'il soit théoriquement possible de continuer à utiliser le client Gmail,
en le connectant sur le compte de l'hébergeur, dans la pratique ce n'est pas
vraiment possible pour des raisons techniques (pour les curieux, le client
Gmail ne permet pas de se connecter à un compte externe en IMAP, mais
uniquement en POP, ce qui revient à utiliser le compte Gmail, chez Google
donc).

Il va donc falloir que Jean utilise un autre client mail, comme
par exemple Thunderbird. Il lui faudra le télécharger, l'installer, et le
configurer (voir en fin d'article l'exemple de l'hébergement chez Alwaysdata).

Il peut autrement préférer utiliser le « webmail » fourni par son hébergeur
(par exemple Roundcube, qui est assez répandu), pour continuer à consulter ses
messages directement sur un site internet, sans avoir à installer de logiciel
sur son ordinateur.

Afin de continuer à recevoir les mails envoyés à *jean.dupont@gmail.com*, il
va falloir qu'il configure une redirection au niveau de Gmail.


Rediriger *jean.dupont@gmail.com* vers *jean@dupont.fr*
-------------------------------------------------------

Cette redirection se met en place par le biais du client Gmail, et est bien
expliquée sur le site du support de Google : `Transfert automatique des
messages vers un autre compte de messagerie`_.

.. _Transfert automatique des messages vers un autre compte de messagerie:
    https://support.google.com/mail/answer/10957?hl=fr&ctx=mail

**ATTENTION :** si vous aviez au préalable mis en place une redirection vers
l'adresse Gmail, il vous faut à présent impérativement la désactiver. Ainsi,
Jean devra désactiver la redirection des mails de *jean@dupont.fr* vers
*jean.dupont@gmail.com*.

Une fois la redirection mise en place sur son adresse *jean.dupont@gmail.com*,
Jean pourra utiliser son nouveau client pour se connecter à son compte chez son
hébergeur.

Tous les mails envoyés à *jean@dupont.fr* ou à *jean.dupont@gmail.com*
arriverons sur son compte chez son hébergeur.


Conclusion
==========

Et demain ? Si jamais Jean décide de changer d'hébergeur ?

Il lui suffira de configurer son nom de domaine pour qu'il pointe vers le
serveur de son nouvel hébergeur (enregistrements *MX*, se reporter à l'article
précédent), puis qu'il y crée un compte pour son adresse mail.

Il lui faudra aussi configurer son client lourd pour qu'il pointe sur le
nouveau compte, ou utiliser le client web fourni par son nouvel hébergeur.

Il n'y aura plus à créer de redirection ou à configurer une adresse
d'expédition, bref, plus de soucis, tout est sous son contrôle, et aucun besoin
de contacter tout son carnet d'adresse pour faire connaître sa nouvelle
adresse.


Informations de connexion à un compte hébergé par Alwaysdata
============================================================

Stratégie timorée
-----------------

Voici comment configurer le client Gmail pour envoyer les mails de la part de
*jean@dupont.fr* (stratégie timorée) :

.. image:: |filename|./images/gmail_alwaysdata_1.png
   :alt: Configuration de Gmail pour l'hébergeur Alwaysdata (1)

.. image:: |filename|./images/gmail_alwaysdata_2.png
   :alt: Configuration de Gmail pour l'hébergeur Alwaysdata (2)


Stratégie courageuse
--------------------

Voici à quoi ressemble la configuration lors de l'ajout d'un compte mail sur
Thunderbird :

.. image:: |filename|./images/thunderbird_alwaysdata.png
   :alt: Configuration de Thunderbird pour l'hébergeur Alwaysdata

Alwaysdata fourni aussi un client web (Roundcube) accessible sur
https://webmail.alwaysdata.com. Il suffit alors d'indiquer son mail et son mot
de passe, aucune autre configuration n'est requise.


La suite
========

Le prochain article donnera des techniques pour `Migrer ses mails`_.
