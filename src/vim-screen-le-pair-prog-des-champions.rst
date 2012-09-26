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
du blog de Siyelo`_, adapté, simplifié et automatisé à ma sauce.


Installer un serveur SSH
~~~~~~~~~~~~~~~~~~~~~~~~

Pour ça, tu es bien gentil, mais je pense que tu vas y arriver tout seul comme
un grand.

Si nécessaire, pour que ton collègue distant puisse se connecter en local,
rajoute donc une règle de redirection sur ton routeur/ta box , par exemple du
port externe ``22222``, en ``TCP``, vers le port ``22`` de l'adresse IP de ton
ordinateur.

.. note:: Il existe un logiciel très pratique pour gérer ses règles de
          redirection sans avoir à se connecter à l'interface de sa box :
          portmapper_ (Korben_ en parle d'ailleurs très bien).


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

L'idée est simple : un utilisateur local (que l'on nommera ``pair``) va lancer
le ``screen``, sur lequel tu pourra te connecter. Il suffira ensuite de donner
le mot de passe de ce compte à ton collègue distant, pour qu'il s'y connecte en
ssh, puis se connecte lui aussi à ce ``screen``.

Cet utilisateur ``pair`` sera donc utilisé pour programmer, voire même
*commiter* le code, avec éventuellement un ``~/.gitconfig`` ou ``~/.hgrc`` avec
un nom évocateur du genre ``pair-benoit-mathieu``, afin que les *commits*
puissent être directement attribués aux bonnes personnes.

Pour créer ce nouvel utilisateur :

.. code-block:: sh

    sudo adduser pair

Enfin, toute la configuration de ``screen`` est mise dans un fichier
``.screenrc`` à la racine du compte :

::

    hardstatus on
    hardstatus alwayslastline
    startup_message off
    termcapinfo xterm ti@:te@
    hardstatus string "%{= kG}%-w%{.rW}%n %t%{-}%+w %=%{..G} %H %{..Y} %m/%d %C%a "
    term screen-256color

    multiuser on
    acladd <ton user>  # user allowed to connect

Prends bien soin de remplacer ``<ton user>`` par ton utilisateur, afin que
lorsque le ``screen`` soit lancé, tu puisse t'y connecter.


Utiliser
~~~~~~~~

Lance un ``screen`` sur l'utilisateur ``pair`` en mode détaché :

.. code-block:: sh

    sudo -u pair screen -d -m -S pairprog  # -S nomme la session

Connecte toi au ``screen`` de cet utilisateur :

.. code-block:: sh

    screen -x pair/pairprog
    # une fois connecté au screen
    vim
    # créer une nouvelle fenêtre dans le screen : <ctrl-a c>
    # passer à la fenêtre suivante : <ctrl-a n>
    # passer à la fenêtre précédente : <ctrl-a p>
    # passer à la fenêtre 1 : <ctrl-a 1>
    # détruire la fenêtre courante : <ctrl-a k> ou <ctrl-d>

Si tu es un vrai bon fainéant comme moi, tu aura bien sûr sauté sur l'occasion
d'en faire un alias dans ton ``~/.bashrc``.

Indique l'utilisateur ``pair`` et son mot de passe, ton adresse IP et le port
de connexion SSH à ton collègue pour qu'il puisse te rejoindre :

.. code-block:: sh

    ssh pair@<ip de ta box> -p 22222
    screen -x pairprog  # alias pair='screen -x pairprog'

Petite astuce de sioux, pour que l'utilisateur distant n'ai même pas besoin de
se connecter manuellement au ``screen`` (ni même à lancer l'alias), à rajouter
au ``~/.bashrc`` de l'utilisateur ``pair``

.. code-block:: sh

    export TERM=xterm-256color  # compatibility with screen

    if [ ${SSH_CLIENT:+x} ]
        clear
        echo "Welcome to the pair-programming session"
        echo -n "Press Enter to continue..." && read
        screen -x pairprog  # pairprog est le nom de la session
    fi

La variable d'environnement ``SSH_CLIENT`` est testée pour que la petite astuce
ne soit utilisée que lors d'une connexion ssh, et non à chaque lancement d'un
``shell``.

Enfin, pour pouvoir dialoguer plus facilement, j'utilise un logiciel de voix
sur IP (ou tout bêtement le téléphone). C'est nettement plus pratique pour
faciliter la communication !


Il ne me reste plus qu'à te souhaiter de te coupler avec un de tes pair, de
vivre heureux, et d'avoir plein de belles lignes de codes !


----


.. target-notes::

.. _`pair-programming`: http://fr.wikipedia.org/wiki/Programmation_en_bin%C3%B4me
.. _screen: http://www.gnu.org/s/screen/
.. _`article du blog de Siyelo`: http://blog.siyelo.com/remote-pair-programming-with-screen
.. _portmapper: http://upnp-portmapper.sourceforge.net/
.. _Korben: http://korben.info/comment-ouvrir-et-mapper-facilement-des-ports-sur-votre-routeur.html
