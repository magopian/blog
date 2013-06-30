Quitter Gmail pour les nuls
###########################
:date: 2013-06-25 08:34
:category: misc


Cet article est le premier d'une série sur les mails. Il est destiné aux
personnes n'ayant pas ou peu de connaissances techniques du domaine, et a pour
but de permettre à chacun de reprendre le contrôle sur son adresse mail.

Nous allons voir la différence entre une adresse mail, un compte mail et un
client mail, et donner des stratégies pour se passer de Gmail.

Les exemples donnés dans cet article se basent sur Gmail, mais ils sont très
largement applicables pour d'autres fournisseurs comme LaPoste.net ou Hotmail.

Pour l'histoire, Jean Dupont, qui utilisait jusqu'à présent son adresse
*jean.dupont@gmail.com*, vient de se procurer un compte mail chez son
hébergeur, ainsi qu'un nom de domaine et une adresse *jean@dupont.fr*.

Nous aborderons dans un futur article ce qui concerne la réservation d'un nom
de domaine et la création d'un compte mail chez un hébergeur, et dans un autre
la gestion des contacts.


Pourquoi
========

À l'heure du *cloud*, du mail facile et du Gmail si pratique et quasi
universel, pourquoi donc vouloir s'en passer ?

Plusieurs raisons :

* les données appartiennent à Google, elles sont sur leurs serveurs, et en font
  ce qu'ils veulent
* ils peuvent décider du jour au lendemain de fermer un compte, sans préavis,
  sans possibilité de négociation
* ils donnent l'accès à tous les mails à la
  :abbr:`NSA (National Security Agency, les services secrets des États-Unis)`
  (et à qui d'autre ?)

Si vous pensez que vous n'avez de toute manière rien à cacher, ou qu'il n'y a
aucune raison qu'on vous ferme votre compte, sachez que les exemples ne
manquent pas.

Il est clair que d'avoir son adresse, son compte et son client mail
tous au même endroit, fournis par la même entité, c'est bien plus pratique,
mais on est alors entièrement dépendant de cette entité : « Il ne faut pas
mettre tous ses œufs dans le même panier ».

Nous allons voir quelles sont les stratégies que Jean Dupont peut mettre en
place pour avoir une adresse mail qu'il contrôle, et qu'il peut faire pointer
où il veut.


Termes et définitions
=====================

Adresse mail
------------

C'est l'équivalent du numéro de téléphone. C'est ce qui permet d'acheminer les
messages au bon endroit.

Avec un numéro de téléphone, on peut joindre n'importe qui, à partir de
n'importe quel opérateur, vers n'importe quel opérateur. L'opérateur n'a aucune
importance, ce qui est important, c'est que tous savent où diriger un appel.

L'adresse mail se rapproche ainsi plus d'un numéro de téléphone que d'une
adresse postale (qui dépends de la localisation, et non de la personne qui
habite à cet endroit).

Il faut donc voir l'adresse mail comme une localisation qui peut changer (le
même numéro pourrait être chez SFR un jour, et chez Bouygues le lendemain).

De la même manière, *jean@dupont.fr*, qui est la propriété de Jean, pointe vers
un compte de son choix. Il pourra le faire pointer ailleurs quand il le
souhaitera, contrairement à l'adresse *jean.dupont@gmail.com* qui appartient à
Google, et qui ne pointera jamais ailleurs.


Compte mail
-----------

C'est l'équivalent de la boite postale dans lequel le facteur dépose votre
courrier. C'est l'endroit où arrivent tous les messages.

Contrairement à la boite postale (qui en général ne sert que temporairement, le
temps de récupérer le courrier), un compte mail peut stocker les messages
aussi longtemps qu'on le souhaite.

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
* trier, ordonner, classer les message

Accessoirement, ce client permet souvent de gérer les adresses (contacts), mais
c'est un autre sujet.

Ce programme se présente généralement sous deux formes différentes :

* le client web : un site, comme par exemple http://mail.google.com

  - s'utilise sur le port 80, qui est rarement bloqué (dans les hôtels, sur les
    accès wifi publics, dans les entreprises...)
  - ne nécessite pas d'installation de logiciel sur son ordinateur
  - ne nécessite pas de configuration (dans le cas où il est fourni directement
    par l'hébergeur du compte utilisé)

* le client lourd : un programme à installer sur son ordinateur, comme par
  exemple Thunderbird_

  - sauvegarde les messages sur l'ordinateur
  - parfois plus pratique et ergonomique qu'un client web
  - peut être utilisé sans connexion à internet : les messages à envoyer sont
    stockés puis envoyés lors de la prochaine connexion
  - n'est pas dépendant d'un hébergeur, et donc tous les mails seront conservés
    le jour d'un changement

.. _Thunderbird: http://www.mozilla.org/fr/thunderbird/?flang=fr

Dans une certaine limite, les clients sont interchangeables. Ainsi, on peut
utiliser le **client** Thunderbird pour accéder à un **compte** Gmail.


Redirection
-----------

C'est un peu comme un suivi de courrier postal : il permet de faire suivre tout
le courrier normalement destiné à une adresse vers une autre adresse.

Ainsi, Jean peut décider de rediriger tous les messages destinés à
*jean@dupont.fr* vers l'adresse *jean.dupont@gmail.com*.

Il est aussi souvent possible, en plus de la redirection, de sauvegarder les
messages sur le compte lié à *jean@dupont.fr*. Ainsi, Jean peut stocker ses
messages sur deux comptes : celui lié à *jean@dupont.fr* (chez son hébergeur),
ainsi que celui lié à *jean.dupont@gmail.com* (chez Google).


Sauvegarde
----------

Il est possible de conserver plusieurs copies de ses messages, afin d'avoir une
sauvegarde en cas de défaillance d'une machine (son ordinateur, la machine de
son hébergeur...).

Exemple : l'utilisation d'un client lourd (comme Thunderbird) permet d'avoir
une copie des message sur son ordinateur, tout en les conservant sur le serveur
(sur le compte). On peut alors envisager de sauvegarder ces messages (qui sont
stockés sous forme de fichiers sur l'ordinateur) sur un disque USB, un NAS, un
compte Dropbox...


Comment
=======

Jean veut avoir le contrôle de la destination de ses messages, afin de pouvoir
changer d'avis si il le souhaite. Il va donc faire passer le mot que sa
nouvelle adresse est désormais *jean@dupont.fr*, et non plus
*jean.dupont@gmail.com*.

Par contre, Jean veut toujours recevoir les mails envoyés à
*jean.dupont@gmail.com*, car il y a beaucoup d'entités qui ne connaissent pas
encore sa nouvelle adresse, comme les impôts, EDF, ou encore des abonnements à
des listes de diffusion.

Avant de rentrer dans le détail, voici les deux stratégies possibles :

* timorée : conserver Gmail comme compte principal
* courageuse : utiliser son nouveau compte comme compte principal

Ces deux étapes sont indépendantes, et il est tout à fait possible de rester à
la première étape.

Il est aussi tout à fait possible de passer directement à la deuxième étape,
sans passer par la première.

Le plus important est de pouvoir utiliser sa nouvelle adresse mail, afin
d'avoir à minima le contrôle de la destination et du stockage des messages.


Stratégie timorée : Conserver Gmail comme compte principal
==========================================================

Cette stratégie est un compromis qui permet de ne pas changer grand chose à ses
habitudes quotidiennes, l'inconvénient étant que Google a toujours accès à tous
les messages, et elle demande plus de configuration.

Elle permet par ailleurs de continuer à utiliser Gmail comme compte principal
pour des raisons pratiques (avoir tous ses messages au même endroit), et le
client Gmail (accessible sur http://mail.google.com).


Rediriger *jean@dupont.fr* vers *jean.dupont@gmail.com*
-------------------------------------------------------

C'est la toute première chose à faire. Sur son hébergeur, il va configurer son
adresse *jean@dupont.fr* pour qu'elle redirige tous les messages vers
*jean.dupont@gmail.com*, un peu comme si il mettait en place un suivi de
courrier postal.

Ainsi, dès que quelqu'un écrira à *jean@dupont.fr*, le message sera
automatiquement transféré, relayé, redirigé vers *jean.dupont@gmail.com* (comme
si il avait été destiné à *jean.dupont@gmail.com* dès le début).

Si son hébergeur le permet, il peut par ailleurs configurer son adresse
*jean@dupont.fr* pour que les messages soient quand même copiés et stockés sur
le compte associé (chez l'hébergeur donc).

Il accédera alors à ses messages toujours de la même manière, en se connectant
sur http://mail.google.com, et il aura toujours une copie de sauvegarde sur le
compte de son hébergeur.

Cette redirection devra rester en place tant que l'adresse
*jean.dupont@gmail.com* sera connue et utilisée, ou tant que la stratégie
courageuse ne sera pas mise en place.


Configurer le client Gmail : envoyer les mails de la part de *jean@dupont.fr*
-----------------------------------------------------------------------------

Par défaut, un client mail envoie tous les mails de la part de l'adresse mail
associée au compte sur lequel le client se connecte.

Ainsi, le client mail de Gmail (http://mail.google.com), qui est connecté au
compte Gmail, qui lui même est associé à l'adresse mail
*jean.dupont@gmail.com*, va automatiquement, par défaut, envoyer tous les mails
de la part de *jean.dupont@gmail.com*.

Prenons le scénario suivant :

* *john@smith.com* envoie un mail à *jean@dupont.fr*
* le mail arrive sur l'hébergeur de Jean, qui après avoir fait une copie sur le
  compte local, redirige le message vers Google (sur *jean.dupont@gmail.com*)
* le mail arrive chez Google (sur le compte Gmail)
* Jean peut voir le nouveau message, le consulter, et y répond
* le client Gmail va donc envoyer une réponse à *john@smith.com*, de la part de
  *jean.dupont@gmail.com*

Et là, c'est le drame. En effet, si John répond à nouveau, il va envoyer
directement le mail à *jean.dupont@gmail.com*. Jean aura beau eu faire part de
sa nouvelle adresse, dans les faits, la plupart des messages continueront à
être directement envoyés à son adresse Gmail.

La solution est donc de configurer le client Gmail pour qu'il envoie tous les
mails de la part de *jean@dupont.fr*.

Il y a une page expliquant comment faire cela : `Envoi de message avec une
autre adresse`_.

.. _Envoi de message avec une autre adresse: https://support.google.com/mail/answer/22370?hl=fr&ctx=mail

Voici une explication résumée :

#. Cliquez sur l'icône représentant une roue dentée en haut à droite de
   l'écran, puis sélectionnez Paramètres
#. Cliquez sur l'onglet Comptes
#. Sous « Envoyer des e-mails en tant que », cliquez sur « Ajouter une autre
   adresse e-mail »
#. Dans le champ « Adresse e-mail », saisissez votre nom (Jean Dupont) et
   l'autre adresse e-mail (*jean@dupont.fr*), et décochez la case « Traiter
   comme un alias »
#. Choisissez l'option « Utiliser les serveurs SMTP de votre autre fournisseur de messagerie »
#. Entrez les informations de connexion au compte de votre hébergeur (voir plus
   loin pour l'exemple de l'hébergement chez AlwaysData)
#. Cliquez sur « Enregistrer les modifications »
#. De retour dans les paramètres du compte, cliquez sur le lien « utiliser par
   défaut » à droite de la nouvelle adresse que vous venez de créer
#. Choisissez enfin, sous « En réponse à un message », l'option « Toujours
   répondre à partir de l'adresse par défaut (actuellement jean@dupont.fr) »

Suite à ce changement, tous les mails qui seront envoyés à partir du client
Gmail seront envoyés de la part de *jean@dupont.fr*, et donc toutes les
personnes qui répondent, répondront directement à cette nouvelle adresse mail.

Tous les mails envoyés à *jean@dupont.fr* ou à *jean.dupont@gmail.com*
arriverons sur son compte chez Google.


Stratégie courageuse : Utiliser son nouveau compte
==================================================

Bien qu'il soit théoriquement possible de continuer à utiliser le client Gmail,
en le connectant sur le compte de l'hébergeur, dans la pratique ce n'est pas
vraiment possible pour des raisons techniques (pour les curieux, le client
Gmail ne permet pas de se connecter à un compte externe en IMAP, mais
uniquement en POP, ce qui revient à utiliser le compte Gmail, chez Google
donc).

Il va donc falloir que Jean commence par utiliser un autre client mail, comme
par exemple Thunderbird. Dans ce cas, il lui faudra le télécharger,
l'installer, et le configurer (voir plus loin pour l'exemple de l'hébergement
chez AlwaysData).

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

.. _Transfert automatique des messages vers un autre compte de messagerie: https://support.google.com/mail/answer/10957?hl=fr&ctx=mail

**ATTENTION :** si vous aviez au préalable mis en place une redirection vers
l'adresse Gmail, il vous faut à présent impérativement la désactiver.

Ainsi, Jean devra désactiver la redirection des mails de *jean@dupont.fr* vers
*jean.dupont@gmail.com*.

Une fois la redirection mise en place sur son adresse *jean.dupont@gmail.com*,
et la redirection désactivée sur *jean@dupont.fr*, Jean pourra utiliser son
client (Thunderbird, ou le client web fourni) pour se connecter à son compte
chez son hébergeur.

Tous les mails envoyés à *jean@dupont.fr* ou à *jean.dupont@gmail.com*
arriverons sur son compte chez son hébergeur.


Conclusion
==========

Et demain ? Si jamais Jean décide de changer d'hébergeur ?

Il n'aura plus aucun soucis : il lui suffira de configurer son adresse mail au
niveau de son nouvel hébergeur, pour qu'elle pointe vers son nouveau compte.

Il lui faudra aussi configurer son client lourd pour qu'il pointe sur le
nouveau compte, ou utiliser le client web fourni par son nouvel hébergeur.

Il n'y aura plus à créer de redirection ou à configurer une adresse
d'expédition, bref, plus de soucis, tout est sous son contrôle.


Informations de connexion à un compte hébergé par AlwaysData
============================================================

Si vous avez choisi AlwaysData_ comme hébergeur, voici les information de
connexion à configurer au niveau du client mail (Thunderbird, ou le client
Gmail lors de la mise en place de l'envoi de message avec une autre adresse) :

.. _AlwaysData: https://alwaysdata.com

Envoi de messages :

* Serveur SMTP : ``smtp.alwaysdata.com``
* Port : ``587``
* Option de sécurité : ``STARTTLS`` ou ``TLS``
* Nom d'utilisateur : ``jean@dupont.fr``
* Mot de passe : le mot de passe choisi lors de la création du compte mail

Connexion au compte :

* Serveur Type : ``IMAP``
* Serveur Name : ``imap.alwaysdata.com``
* Port : ``993``
* Option de sécurité : ``STARTTLS`` ou ``TLS``
* Nom d'utilisateur : ``jean@dupont.fr``
* Mot de passe : le mot de passe choisi lors de la création du compte mail

Stratégie timorée
-----------------

Voici comment configurer le client Gmail pour envoyer les mails de la part de
*jean@dupont.fr* (stratégie timorée) :

.. image:: |filename|./images/gmail_alwaysdata_1.png
   :alt: Configuration de Gmail pour l'hébergeur AlwaysData (1)

.. image:: |filename|./images/gmail_alwaysdata_2.png
   :alt: Configuration de Gmail pour l'hébergeur AlwaysData (2)


Stratégie courageuse
--------------------

Voici à quoi ressemble la configuration lors de l'ajout d'un compte mail sur
Thunderbird :

.. image:: |filename|./images/thunderbird_alwaysdata.png
   :alt: Configuration de Thunderbird pour l'hébergeur AlwaysData

AlwaysData fourni aussi un client web (Roundcube) accessible sur
https://webmail.alwaysdata.com. Il suffit alors d'indiquer son mail et son mot
de passe, aucune autre configuration n'est requise.


.. note:: Je n'ai aucun intéressement chez Alwaysdata_, si je les prend en
          exemple c'est que je suis un client satisfait.
