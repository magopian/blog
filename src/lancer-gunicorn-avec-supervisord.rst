lancer gunicorn avec supervisord
################################
:date: 2010-08-31 16:48
:category: django

Après avoir mis en place une méthode pour `lancer gunicorn avec runit`_,
voici un second article pour lancer ce même `gunicorn`_ (qui poutre du
poney, rappelons-le), mais avec un outil que je trouve à l'utilisation
bien plus pratique : `supervisord`_

Pourquoi supervisord et pas runit ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Après l'avoir utilisé sans aucun soucis depuis quelques temps sur le
serveur de secours de notre site web, je trouve que supervisord est plus
convivial à utiliser, et plus "clair" à mettre en place.

Plus convivial à utiliser parce qu'il a un client CLI qui permet
d'interagir directement avec les processus monitorés, mais il y a aussi
les mêmes fonctionnalités par le biais d'une interface web fort
pratique.

Plus "clair" à mettre en place parce qu'il se lance grâce à un simple
script d'init, et qu'on peut faire la configuration de tous ses
processus à monitorer dans un seul et même fichier de configuration, au
lieu d'avoir un répertoire et des liens symboliques à gérer (certains
préfèrent peut-être cette modularité, mais personnellement je trouve ça
beaucoup plus pénible à maintenir).

Installer supervisord
^^^^^^^^^^^^^^^^^^^^^

Etant donné que supervisord est en python, il est possible de
l'installer avec un simple

::

    $ pip install supervisor

Pour les *old-school* qui ne profitent pas encore de la puissance et de
l'ergonomie de ce magnifique outil de Ian Bicking, il est possible de
remplacer *pip* par *easy\_install* (même si je vous conseille plutôt de
faire un *easy\_install pip* puis de vous passer de *easy\_install* par
la suite!).

Configurer supervisord
^^^^^^^^^^^^^^^^^^^^^^

On le configure en deux temps : une première configuration de
supervisord lui-même, puis l'ajout des processus qu'on veut qu'il
monitore.

Dans le fichier */etc/supervisord.conf* :

::

    ; configuration de supervisord lui-meme
    [unix_http_server]
    file=/tmp/supervisor.sock   ; chemin vers le fichier socket

    [inet_http_server]
    port=192.168.0.21:9001      ; adresse ip _LOCALE_ de la machine pour la connection web

    [supervisord]
    logfile=/var/log/supervisord.log ; fichier de log principal de supervisord

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [supervisorctl]
    serverurl=unix:///tmp/supervisor.sock ; connection pour le client CLI

    ; liste des processus qu'on veut confier a supervisord
    [program:gu-www]
    command=/path/to/venv/bin/python /path/to/venv/bin/gunicorn_django -b localhost:8080 --log-file=/path/to/log/gunicorn_gu-www.log --workers=3
    directory=/folder/containing/settings/file/
    user=www-data
    autostart=true
    autorestart=true
    startsecs=10
    redirect_stderr=true
    stdout_logfile=/path/to/log/supervisor_gu-www.log

Bien entendu, faites en sortes que l'utilisateur *www-data* ai accès en
écriture aux fichiers de log *gunicorn\_gu-www.log* configuré où le
processus échouera lors de son lancement.

**ATTENTION:** comme indiqué dans le commentaire pour la ligne de
configuration *inet\_http\_server* il faut absolument faire en sorte que
l'adresse ne soit pas accessible à tout le monde! En effet il est
possible de redémarrer ou tout simplement stopper les processus par
cette interface! Vous pouvez désactiver complètement cette possibilité
en supprimant ces deux lignes, il n'y aura alors pas de moyen de
contrôler supervisord par une page web.

La commande indiquée pour information lance *gunicorn\_django* avec
dans un environnement virtuel (ce que vous devriez faire vous aussi!).
Il n'est pas nécessaire d'indiquer le chemin vers le fichier
*settings.py* dans les options de *gunicorn\_django* étant donné que le
processus sera lancé directement dans le répertoire le contenant (si
vous le configurez correctement avec le paramètre *directory* comme
indiqué ci-dessus).

**ATTENTION:** il faut absolument que *gunicorn\_django* soit lancé en
*foreground* (en tâche principale, pas en
*arrière-plan*/*background*/*démon*/*daemon*), ce qui est le cas par défaut
si vous n'avez pas explicitement dit le contraire dans votre fichier de
configuration (ou en paramètre de la commande) de *gunicorn\_django*.

En effet c'est *supervisord* qui se charge de le faire : si le
processus est lancé en arrière-plan, *supervisord* ne peut pas prendre
la main dessus et le contrôler ni le monitorer, et va essayer de le
lancer plusieurs fois d'affilée pensant qu'il échoue à chaque fois.

Lancer supervisord et le relancer à chaque reboot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Il suffit pour cela de créer un script de démarrage dans */etc/init.d/*
et de le faire se lancer à chaque démarrage.

Dans */etc/init.d/supervisord* :

::

    #! /bin/sh
    ### BEGIN INIT INFO
    # Provides:          supervisord
    # Required-Start:    $remote_fs
    # Required-Stop:     $remote_fs
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: Example initscript
    # Description:       This file should be used to construct scripts to be
    #                    placed in /etc/init.d.
    ### END INIT INFO

    # Author: Dan MacKinlay
    # Based on instructions by Bertrand Mathieu
    # http://zebert.blogspot.com/2009/05/installing-django-solr-varnish-and.html

    # Do NOT "set -e"

    # PATH should only include /usr/* if it runs after the mountnfs.sh script
    PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin
    DESC="supervisord"
    NAME=supervisord
    DAEMON=supervisord
    MANAGE=supervisorctl
    DAEMON_ARGS=""
    PIDFILE=/var/run/$NAME.pid
    SCRIPTNAME=/etc/init.d/$NAME

    # Load the VERBOSE setting and other rcS variables
    . /lib/init/vars.sh

    # Define LSB log_* functions.
    # Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
    . /lib/lsb/init-functions

    case "$1" in
      start)
        $DAEMON
            ;;
      stop)
        $MANAGE shutdown
            ;;
      reload|force-reload)
        $MANAGE reload
        ;;
      restart)
        $MANAGE restart
            ;;
      *)
            echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
            exit 3
            ;;
    esac

Ce script contient des commentaires en début de fichier qui permettent
de le faire se lancer automatiquement à chaque démarrage :

::

    $ chmod a+x /etc/init.d/supervisord
    $ update-rc.d supervisord defaults 99 # le chiffre fourni est la priorité

Cette commande devrait indiquer qu'elle a créé tous les liens
symbolique nécessaire pour lancer ce script à chaque démarrage du
serveur. La priorité est le chiffre utilisé pour le nom du lien
symbolique (S99supervisord, K99supervisord...). Les scripts sont lancés
dans l'ordre croissant de ces chiffres : si on veut que supervisord se
lance dans les derniers (recommandé, pour que tous les services
indispensables soient déjà lancés), il faut un chiffre élevé.

Il ne reste plus qu'à lancer *supervisord* maintenant et vérifier que
notre site est accessible :

::

    $ /etc/init.d/supervisord start

Monitorer et contrôler ses processus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Soit en utilisant le client CLI :

::

    $ supervisorctl

Soit en accédant à la page web dont on a configuré l'adresse dans le
paramètre *inet\_http\_server* dans le fichier de configuration de
*supervisord*. De là vous pouvez redémarrer vos processus, les arrêter,
visualiser le contenu du fichier de log...

Un soucis?
^^^^^^^^^^

-  Pensez à regarder dans les fichiers de log indiqués dans les
   paramètres pour voir si il y a des indications sur le problème
-  Vérifiez que la commande configuré dans /etc/*supervisord.conf* se
   lance correctement manuellement, et que le processus est bien en
   *foreground*
-  Faites un tour sur l'excellente documentation du `projet supervisord`_

Edit du 2010-12-14 : rajout de la priorité de lancement lors de l'appel
de la commande *update-rc.d*


.. _lancer gunicorn avec runit: ./lancer-gunicorn-avec-runit.html
.. _gunicorn: http://gunicorn.org/
.. _supervisord: http://supervisord.org/index.html
.. _projet supervisord: http://supervisord.org/
