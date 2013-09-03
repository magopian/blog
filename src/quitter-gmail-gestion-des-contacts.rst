Quitter Gmail : gestion des contacts
####################################
:date: 2013-08-06 09:14
:category: misc


Cet article est le cinquième d'une série sur comment reprendre le contrôle sur
son mail, et quitter son fournisseur de mail centralisé.

#. `Pourquoi quitter Gmail`_
#. `Réserver son propre nom de domaine`_
#. `Créer son compte mail`_
#. `Migrer ses mails`_
#. Gestion des contacts

.. _Pourquoi quitter Gmail: |filename|./quitter-gmail.rst
.. _Réserver son propre nom de domaine:
    |filename|./quitter-gmail-reserver-son-nom-de-domaine.rst
.. _Créer son compte mail: |filename|./quitter-gmail-creer-son-compte-mail.rst
.. _Migrer ses mails: |filename|./quitter-gmail-migrer-ses-mails.rst

La gestion des contacts est un peu plus complexe que ce que nous avons pu voir
jusqu'à présent.

En effet, il n'y a malheureusement pas de moyen simple, pour le moment, d'avoir
les mêmes avantages qu'avec Google.

Il existe tout de même plusieurs stratégies possibles, selon les cas
d'utilisation.

Commençons par quelques définitions.

Termes et définitions
=====================

vCard
-----

Le standard vCard_ est un format d'échange de données personnelles, ce qu'on
appelle couramment les « contacts ».

.. _vCard: http://fr.wikipedia.org/wiki/VCard

Pour exporter ses contacts Gmail dans ce format, et en faire ainsi une
sauvegarde, vous pouvez consulter la page d'aide `Exportation de contacts
Gmail`_.

.. _Exportation de contacts Gmail:
    https://support.google.com/mail/answer/24911?hl=undefined

Il faut surtout se rappeler d'exporter au format vCard, ce qui stockera tous
les contacts dans un fichier avec l'extension ``.vcf``.


CardDav
-------

CardDav_ est un protocole d'échange de vCard, basé sur le modèle
client/serveur.

.. _CardDav: http://fr.wikipedia.org/wiki/CardDAV

Cela signifique que pour en profiter, il faut un serveur qui stocke les vCard
(les informations des contacts), et les clients peuvent ensuite s'y connecter
pour récuperer ces informations, ou les mettre à jour.

On a alors une synchronisation des contacts sur les différents clients
(téléphone mobile, Thunderbird sur l'ordinateur...).


Comment
=======

Rapatrier ses contacts
----------------------

Nous avons vu dans la définition de vCard, qu'il est possible d'exporter tous
les contacts de Gmail dans un fichier. Malheureusement, ce fichier n'est pas
bien importé par Thunderbird à l'heure actuelle.

Pour information, une refonte complète de la partie gestion de contacts est en
cours pour Thunderbird : Ensemble_.

.. _Ensemble: https://github.com/mikeconley/thunderbird-ensemble

En attendant, pour récupérer proprement tous les contacts de Gmail sur
Thunderbird, il est recommandé d'utiliser le `module complémentaire`_
Thunderbird `Google contacts`_.

.. _module complémentaire:
    https://support.mozillamessaging.com/fr/kb/faq-des-modules-complementaires
.. _Google contacts:
    https://addons.mozilla.org/en-US/thunderbird/addon/google-contacts/

Une fois installé dans Thunderbird, il faut le configurer : dans la gestion des
modules complémentaires, il y a un bouton à droite du module Google Contacts.

Y rajouter son compte Gmail, est le reste se fera tout seul.


Exporter/importer depuis son téléphone mobile
---------------------------------------------

Voilà une méthode plus laborieuse, mais si les contacts sont rarements mis à
jour, c'est la solution la plus simple.

Elle consiste à échanger des fichiers ``.vcf``, en exportant ses contacts d'une
source, et les important dans une autre.


iPhone
~~~~~~

* importer : envoyer le fichier ``.vcf`` par mail, l'ouvrir sur son iPhone, et
  importer tous les contacts
* exporter : à ma connaissance un seul moyen si on utilise pas iTunes,
  l'application MyContactsBackup_

.. _MyContactsBackup:
    https://itunes.apple.com/en/app/my-contacts-backup/id446784593?mt=8


Android
~~~~~~~

Envoyer le fichier sur le téléphone (par exemple par connexion USB, ou par
email puis sauvegarde dans le téléphone).

Ensuite ouvrir le carnet d'adresse, puis le menu :

* importer : choisir ``Importer/Exporter » Importer`` depuis la mémoire
* exporter : choisir ``Importer/Exporter » Exporter`` vers la mémoire

Tout comme pour l'iPhone, il est possible d'ouvrir directement un fichier
``.vcf`` en pièce jointe d'un mail.


Thunderbird
~~~~~~~~~~~

Installer le module complémentaire MoreFunctionsForAddressBook_ dans
Thunderbird. Dans une future version de Thunderbird, la gestion des vCard
devrait être plus aboutie, et ne plus nécessiter d'ajout de module
complémentaire.

.. _MoreFunctionsForAddressBook:
    https://freeshell.de//~kaosmos/morecols-en.html

Ensuite, dans le carnet d'adresse, dans le menu ``Outil »
MoreFunctionsForAddressBook » Actions for contacts``

* importer : sélectionner ``Import vCard/vcf``
* exporter : sélectionner ``Export » as vCard (.vcf)``


Synchronisation directe
-----------------------

Elle consiste à connecter son téléphone directement avec l'ordinateur qui fait
tourner Thunderbird, et à lancer la synchronisation manuellement.

L'avantage est que les contacts sur le téléphone mobile et sur Thunderbird sont
synchronisés dans les deux sens.

L'inconvénient est qu'il faut passer par un logiciel annexe, ou par des modules
complémentaires pour Thunderbird, et une application sur son téléphone.

N'ayant pu tester ces solutions, je ne peux les recommander, et elles me
paraissent peu fiables et difficiles d'utilisation. Voici néanmoins quelques
liens :

* Roger4apps_ : module complémentaire pour Thunderbird et application pour
  téléphones Android
* MyPhoneExplorer_ : logiciel compatible windows et Android uniquement, qui ne
  nécessite pas de module complémentaire Thunderbird

.. _Roger4apps: https://sites.google.com/site/roger4apps/
.. _MyPhoneExplorer: http://www.fjsoft.at/en/


Synchronisation par CardDav
---------------------------

C'est la solution la plus pratique et la plus aboutie, celle que vous utilisez
probablement déjà à l'heure actuelle.

En effet, les iPhones synchronisent par défaut automatiquement vers iCloud, et
les Android vers Google, qui fournissent tous les deux un serveur CardDav.

Voici quelques serveurs CardDav :

* OwnCloud_ : il faut l'installer soi-même, ou "louer" une installation chez un
  hébergeur
* iCloud: ``https://contacts.icloud.com``
* Google_: ne fonctionne que pour iOS?

.. _OwnCloud: http://owncloud.org
.. _Google: https://support.google.com/mail/answer/2753077?hl=fr


iPhone
~~~~~~

Il est possible de synchroniser les contacts de son iPhone avec ses contacts
Google : `Synchroniser les contacts avec votre appareil iOS`_.

.. _Synchroniser les contacts avec votre appareil iOS:
    https://support.google.com/mail/answer/2753077?hl=fr

On peut bien entendu utiliser cette même méthode avec n'importe quel serveur
CardDav.


Android
~~~~~~~

Il faut passer par une application tierce : CardDav-Sync_.

.. _CardDav-Sync:
    https://play.google.com/store/apps/details?id=org.dmfs.carddav.sync&hl=en


Thunderbird
~~~~~~~~~~~

Là aussi, il faut passer par un module complémentaire : `SOGo Connector`_.

.. _SOGo connector: http://www.sogo.nu/english/downloads/frontends.html

Il existe un tutoriel_ pour l'installer et l'utiliser avec OwnCloud, mais on
peut l'utiliser pour se connecter à n'importe quel serveur CardDav.

.. _tutoriel:
    http://pedia.zaclys.com/Synchronisation-des-contacts-entre-Thunderbird-et-Owncloud-avec-SOGo-connector,p54,276

D'après mes tests, par contre, le module complémentaire fonctionne de manière
aléatoire, et surtout, ne fonctionne pas du tout avec Google. Il est possible
que les décisions récentes de Google d'abandonner les standards ouverts
(CardDav, CalDav...) y soient pour quelque chose.

Pour la synchronisation avec google, il faut donc se contenter du module
complémentaire indiqué dans le chapitre « rapatrier ses contacts ».


La suite
========

Ma préférence personnelle va vers l'utilisation d'un serveur CardDav. C'est la
seule solution qui me paraît perenne, pratique, et qui égale la facilité de
synchronisation de contacts fournie par Google.

Quel que soit le serveur CardDav utilisé, hormis si c'est sa propre
installation de OwnCloud ou équivalent, on confie et on donne accès à ses
contacts a l'hébergeur, ce qui ne fait que déplacer le problème.

Néanmoins, l'avantage d'avoir ses contacts synchronisés partout est d'avoir
autant de sauvegardes.

La solution la plus pratique à l'heure actuelle semble être OwnCloud_, qu'il
est possible d'installer, par exemple, sur une petite Raspberry-Pi_ qui
consomme très peu, et peut ainsi servir de serveur de sauvegarde personnel à la
maison pour un coût réduit.

.. _Raspberry-Pi: http://www.raspberrypi.org/


Quelques projets à surveiller
=============================

- OwnCloud_ : serveur CardDav (contacts), CalDav (calendrier), sauvegarde de
  fichiers (à la Dropbox)
- mailpile_ : projet opensource visant à remplacer le client GMail
- caliop_ : projet naissant visant à fournir des outils et une plateform pour
  les emails que les utilisateurs puissent utiliser avec confiance
- radicale_ : serveur CardDav et CalDav opensource
- yunohost_ : distribution linux à installer sur un serveur, fournissant une
  installation facile de OwnCloud, Jappix (réseau social), RoundCube (client
  mail web)
- sovereign_ : recettes permettant d'installer les logiciels nécessaires sur un
  serveur pour s'héberger soi-même. Très complet, permet d'avoir son propre
  serveur mail, son hébergement de site web, OwnCloud, VPN, sauvegarde de
  fichiers...

.. _mailpile: http://www.mailpile.is/
.. _caliop: http://www.caliop.net/
.. _yunohost: http://yunohost.org/
.. _radicale: http://radicale.org/
.. _sovereign: https://github.com/al3x/sovereign
