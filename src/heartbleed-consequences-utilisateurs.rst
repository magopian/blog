Heartbleed, conséquences pour les utilisateurs
##############################################
:date: 2014-04-09 09:11
:category: misc


Le problème
===========

Hier, le 8 avril 2014, une énorme faille de sécurité a été divulguée, nom de
code Heartbleed (plus d'infos sur http://heartbleed.com). Elle impacte OpenSSL,
qui est la technologie qui permet de sécuriser les échanges entre notre
navigateur et les sites qui utilisent des adresses qui commencent par
"https://" (notez bien le "s" final). On estime qu'elle impacte environ 2/3
des sites sur internet.

Ces sites qui utilisent SSL apparaissent avec un petit cadenas à gauche de leur
adresse, dans la barre d'adresse de votre navigateur, indiquant que la
connexion est sécurisée. C'est par exemple le cas des sites de banque, de mail,
mais aussi de la plupart des pages de connexion avec mot de passe, et de
paiement par carte bancaire.

Cette sécurité permet de chiffrer toutes les communications entre le navigateur
et le site, empêchant quiconque de pouvoir espionner (par exemple en "sniffant"
le wifi sur lequel vous êtes connectés) et récupérer vos mots de passe.

Seulement voilà, hier on a appris que cette sécurité comportait un bug logiciel
qui permet à n'importe qui de récupérer les mots de passe des utilisateurs et
plein d'autres informations sur les sites qui utilisent cette sécurité.

Petite note pour les utilisateurs de Google Chrome : je vous recommande
d'utiliser Firefox_. Si vous souhaitez continuer à utiliser Chrome, veillez à activer
l'option `vérifier la révocation du certificat serveur`_. Malheureusement,
Chrome a choisi de ne pas activer cette vérification par défaut pour permettre
aux pages de se charger plus vite... au dépends de votre sécurité donc.

.. _Firefox: http://www.mozilla.org/fr/firefox/new/
.. _vérifier la révocation du certificat serveur:
    https://support.google.com/chrome/answer/100214?hl=fr


Ce qu'il faut faire
===================

La plupart des sites ont dû mettre en place un correctif à présent, en tout cas
je l'espère. Pour le vérifier, avant de vous connecter sur un site (n'importe
quel site !!!), vérifiez d'abord qu'il n'est pas (ou plus) vulnérable en
entrant son adresse sur le site suivant : http://filippo.io/Heartbleed/.

Dans tous les cas, je vous recommande de vous déconnecter et reconnecter sur
tous les sites sur lesquels vous êtes déjà connectés, pour être sûr d'avoir la
version la plus à jour de leur connexion SSL, puis de changer vos mots de passe
(oui, tous). Ça va être long et pénible, mais c'est nécessaire. Faites bien la
liste des sites sur lesquels vous vous êtes connectés hier (le 8 avril 2014),
et surveillez bien vos comptes sur ces sites, que vous ne voyez rien de bizarre
qui pourrait être causé par un pirate qui aurait récupéré vos accès (ajout de
bénéficiaires de virement sur votre site bancaire, de nouvelles adresses
d'expédition sur les sites de vente en ligne...).

Pour rappel, deux choses qui vous simplifient la vie concernant les mots de
passe :

#. sur Firefox vous pouvez sauvegarder vos mots de passe dans le navigateur, et
   il faut bien penser à activer le `mot de passe général`_ : un mot de
   passe qui permet de chiffrer tous les mots de passe que vous
   avez enregistrés, pour que quelqu'un qui récupère votre ordinateur (suite à
   un vol, parce qu'il est en réparation, en prêt...) ne puisse pas voir tous
   vos mots de passe enregistrés
#. sur Firefox il est possible de sauvegarder/synchroniser tous ses mots de
   passe enregistrés, ses extensions installées, ses onglets ouverts et ses
   favoris sur un serveur entièrement chiffré et sécurisé de Mozilla en
   utilisant la fonctionnalité `firefox sync`_, que je vous recommande. C'est
   très pratique quand on a plusieurs ordinateurs/téléphones/tablettes avec
   firefox. Faites bien attention de sauvegarder la "clé de récupération Sync"
   pour pouvoir vous reconnecter à votre compte Sync si jamais vous changez
   d'ordinateur (c'est un fichier qu'il faut sauvegarder et garder en lieu
   sûr).
#. il existe de multiples logiciels de gestion de mots de passe, comme
   1password_ ou revelation_ (pour linux). Ils permettent d'enregistrer les
   mots de passe pour tous ses sites, et les sauvegarder dans un fichier
   chiffré. Il faut bien sauvegarder ce fichier (comme pour la clé de
   récupération Sync). C'est très pratique pour retenir tous ses mots de passe,
   en sachant que vous êtes sensé(e)s avoir un mot de passe sécurisé et
   différent sur chacun des sites que vous fréquentez. Autrement, si un de ces
   sites se fait pirater, le pirate peut réutiliser votre mot de passe sur tous
   les autres sites que vous utilisez... Et les sites qui se font pirater
   chaque année sont légion, et il existe des bases de données publiques de
   tous les comptes et mots de passe déjà piratés/connus.

.. _mot de passe général:
    https://support.mozilla.org/fr/kb/utiliser-mot-passe-principal-proteger-identifiants
.. _firefox sync:
    https://support.mozilla.org/fr/kb/comment-configurer-firefox-sync
.. _1password: https://agilebits.com/onepassword
.. _revelation: http://revelation.olasagasti.info/

Pour terminer, sur les sites qui le proposent, activez l'authentification en
deux étapes, comme par exemple sur gmail. C'est une vérification en deux temps
lorsque vous vous connectez ou que vous voulez faire une action sensible sur un
site. Dans un premier temps vous entrez votre mot de passe (qui aurait pu être
piraté), et dans un deuxième temps, vous fournissez un code qui vous a été
donné lors de votre connexion par un autre moyen. Par exemple dans le cas de
gmail, vous installez une application "google authenticator" sur votre
téléphone, qui génère une nouvelle séquence de chiffres chaque minute. Le
pirate doit donc avoir votre mot de passe ET votre téléphone si il veut se
connecter sur votre compte.

Plusieurs sites bancaires permettent aussi cette authentification en deux
étapes.


Allez, c'est maintenant l'heure de changer tous vos mots de passe, courage !
