Vim + Screen : le pair-prog des champions !
###########################################
:date: 2012-09-26 08:43
:category: misc

Le `pair-programming`_ fait partie des bonnes pratiques du développement, ce
n'est plus à prouver : il permet de produire un code de meilleure qualité,
mieux pensé et construit.

On entend souvent dire qu'il est (deux fois) moins productif, vu qu'on est deux
à produire un seul morceau de code, mais dans la pratique, il permet au
contraire d'éviter des pièges ou bugs qui auraient pris un temps fou à
résoudre.

Un autre avantage est de pouvoir mettre le pied à l'étrier d'un autre
développeur sur son code, tout en douceur et efficacement. Ou encore de
partager la paternité, la connaissance et l'expertise sur une base de code,
entre plusieurs développeurs.

Et d'une manière générale, c'est tellement plus sympathique et agréable de
pouvoir réfléchir à deux, discuter, échanger, se conseiller mutuellement !

Bref, comme je le disais, les mérites du pair-programming ne sont plus à
prouver.

Mais comment en profiter quand on travaille à distance ? Je pense par
exemple aux personnes en télé-travail, ou qui veulent participer à des sprints
à distance.

Tu l'as deviné (facile, c'est dans le titre), grâce à VIM (ou tout autre
éditeur en ligne de commande, comme par exemple l'autre dont on ne saurait
prononcer le nom), le logiciel screen_, tout ça sur SSH.

Je te fais ici un résumé de ce qui a été très bien expliqué dans un `article
du blog de Siyelo`_.


Installer un serveur SSH
~~~~~~~~~~~~~~~~~~~~~~~~

Pour ça, tu es bien gentil, mais je pense que tu vas y arriver tout seul comme
un grand.

Si nécessaire, pour que ton collègue distant puisse se connecter en local,
rajoute donc une règle de redirection sur ton routeur/ta box , par exemple du
port externe ``22222``, en ``TCP``, vers le port ``22`` de l'adresse IP de ton
ordinateur.


Installer screen
~~~~~~~~~~~~~~~~

Là encore, rien de bien compliqué.

``screen`` permet de multiplexer plusieurs ``shells``. C'est aussi lui qui va
rendre possible de se connecter à plusieurs sur un seul et même ``shell``,
celui par exemple qui lancera l'éditeur. Cela permet donc dans la pratique de
pouvoir éditer un fichier à plusieurs, et de voir instantanément toutes les
modifications.


Configurer
~~~~~~~~~~

Nommons ici *hôte* l'utilisateur local qui va lancer le screen, et *client*
l'utilisateur local sur lequel va se connecter le collègue distant par ssh, et
qui se connectera au ``screen`` lancé par l'hôte donc.

.. note:: **ATTENTION**, l'utilisateur client (et donc le collègue distant
          connecté sur le compte de l'utilisateur client) aura le même accès,
          les mêmes droits et permissions, une fois connecté sur le screen
          lancé par l'hôte, que l'hôte lui-même. Il est donc prudent de créer
          un utilisateur hôte pour l'occasion, qui n'ait pas accès aux données
          personnelles de votre compte.


L'hôte
------

Toute la configuration de ``screen`` peut être mise dans un fichier
``.screenrc`` à la racine du compte :


::

    hardstatus on
    hardstatus alwayslastline
    startup_message off
    termcapinfo xterm ti@:te@
    hardstatus string "%{= kG}%-w%{.rW}%n %t%{-}%+w %=%{..G} %H %{..Y} %m/%d %C%a "
    term screen-256color

    multiuser on
    acladd pair  # user "pair" allowed to connect


Le client
---------

Pour créer un nouvel utilisateur client, nommé ``pair`` dans notre exemple :

.. code-block:: sh

    sudo adduser pair

Petite astuce : pour que le collègue distant, une fois connecté en local, soit
automatiquement connecté sur le ``screen`` lancé par l'hôte, rajoute les
lignes suivantes au ``.bashrc`` de l'utilisateur client :

::

    export TERM=xterm-256color  # compatibility with screen

    trap "" 2 3 19
    clear
    echo "Welcome to the pair-programming session"
    echo -n "Press Enter to continue..." && read
    screen -x <hote>/pairprog

Remplace ``<hote>`` par le nom de l'utilisateur hôte (ton nom d'utilisateur
si tu n'es pas prudent, et que tu n'as pas suivi le conseil de la note
ci-dessus).


Utiliser
~~~~~~~~

Connecte toi à l'utilisateur hôte et lance le ``screen``

.. code-block:: sh

    sudo su - <hote>
    screen -t pairprog
    # dans le screen
    vim
    # créer une nouvelle fenêtre dans le screen : <ctrl-a c>
    # passer à la fenêtre suivante : <ctrl-a n>
    # passer à la fenêtre précédente : <ctrl-a p>
    # passer à la fenêtre 1 : <ctrl-a 1>
    # détruire la fenêtre courante : <ctrl-a k> ou <ctrl-d>

Indique l'utilisateur client et son mot de passe, ton adresse IP et le port de
connexion SSH à ton collègue pour qu'il puisse te rejoindre

.. code-block:: sh

    ssh pair@<ip de ta box> -p 22222

Pour pouvoir dialoguer plus facilement, j'utilise un logiciel de voix sur IP
(ou tout bêtement le téléphone). C'est nettement plus pratique pour faciliter
la communication !


Il ne me reste plus qu'à te souhaiter de te coupler avec un de tes pair, de
vivre heureux, et d'avoir plein de belles lignes de codes !

----


.. target-notes::

.. _`pair-programming`: http://fr.wikipedia.org/wiki/Programmation_en_bin%C3%B4me
.. _screen: http://www.gnu.org/s/screen/
.. _`article du blog de Siyelo`: http://blog.siyelo.com/remote-pair-programming-with-screen
