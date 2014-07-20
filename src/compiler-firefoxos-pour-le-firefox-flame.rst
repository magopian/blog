Compiler FirefoxOS pour le Firefox Flame
########################################
:date: 2014-07-19 13:52
:category: misc

J'ai reçu mon `Firefox Flame`_ il y a peu, et étant donné que je cherche à en
faire mon téléphone principal, je me suis mis en tête d'installer la dernière
version de FirefoxOS.

.. _Firefox Flame:
    https://developer.mozilla.org/en-US/Firefox_OS/Developer_phone_guide/Flame

En effet la version installée de base sur le Flame est la 1.3, et il y a de
nombreuses limitations. Petit spoiler : la version 2.1 nightly que j'ai
installé en a beaucoup aussi (mais moins, et le téléphone a l'air bien plus
réactif).

Je vais lister ici les étapes que j'ai suivies sur mon *Ubuntu 14.04* pour
compiler la dernière version de FirefoxOS et l'installer sur un *Firefox Flame*
initialement en version 1.3 FR.

Cet article est une recette simplifiée de ce que j'ai pu lire sur le wiki_, qui
est très bien fait et doit être pris comme référence.

.. _Wiki: https://developer.mozilla.org/en-US/Firefox_OS


Installer les prérequis
=======================

https://developer.mozilla.org/en-US/Firefox_OS/Firefox_OS_build_prerequisites#Ubuntu_13.10

..

    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install --no-install-recommends autoconf2.13 bison bzip2 ccache curl flex gawk gcc g++ g++-multilib gcc-4.6 g++-4.6 g++-4.6-multilib git lib32ncurses5-dev lib32z1-dev zlib1g:amd64 zlib1g-dev:amd64 zlib1g:i386 zlib1g-dev:i386 libgl1-mesa-dev libx11-dev make zip libxml2-utils


Configuration
=============

Configurer *ccache* ::

    ccache --max-size 10GB

Désactiver le verrouillage de l'écran (l'outil de communication avec le
téléphone, *adb*, ne peut se connecter qu'avec un téléphone déverrouillé) ::

    Paramètres > Affichage > Délai de l'écran de veille > Jamais

`Installer adb`_ ::

    sudo apt-get install android-tools-adb

.. _Installer adb:
    https://developer.mozilla.org/en-US/Firefox_OS/Debugging/Installing_ADB


Configurer le débuguage à distance (par USB en utilisant *adb*) ::

    Paramètres > Informations > Plus d'informations > Développement > Débogage distant

`Ajouter les règles udev`_ ::

    cat <<EOF>> android.rules
    SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", MODE="0666", GROUP="plugdev"
    SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"
    EOF

    $ sudo mv android.rules /etc/udev/rules.d/
    $ sudo service udev restart

.. _Ajouter les règles udev:
    https://developer.mozilla.org/en-US/Firefox_OS/Firefox_OS_build_prerequisites#For_Linux.3A_configure_the_udev_rule_for_your_phone

Vérifier que *adb* peut se connecter ::

    $ adb devices
    List of devices attached
    1de65791  device

.. note:: Il faut que le téléphone soit déverouillé pour que *adb* puisse s'y
          connecter. Étant donné que plusieurs étapes lors du build/flash
          nécessitent l'accès au téléphone, et ce pendant de longues périodes,
          il est fortement recommandé de totalement désactiver le verouillage
          automatique du téléphone, quitte à la réactiver par la suite.


Sauvegarder le téléphone
========================

https://developer.mozilla.org/en-US/Firefox_OS/Firefox_OS_build_prerequisites#Backup_the_phone_system_partition

..

    mkdir -p flame/backup-flame/
    cd flame
    adb pull /system/ backup-flame/system  # 297Mo
    adb pull /data/ backup-flame/data  # 13Mo
    adb pull /vendor/ backup-flame/vendor  # 47Mo


Se préparer pour le premier build
=================================

https://developer.mozilla.org/en-US/Firefox_OS/Preparing_for_your_first_B2G_build#Clone_B2G_repository

Cloner le dépôt ::

    git clone git://github.com/mozilla-b2g/B2G.git && cd B2G

`Changer les compilateurs par défaut`_ pour ce projet ::

    cat <<EOF>> .userconfig
    # Change the default host compiler.
    export CC=gcc-4.6
    export CXX=g++-4.6
    # Various optional settings.
    export DEVICE_DEBUG=1  # Enable developer mode.
    #export B2G_DEBUG=1  # build a debug build.
    #export MOZ_PROFILING=1  # enable profiling (don't pair with B2G_NOOPT).
    #export B2G_NOOPT=1  # No optimizer.
    #export NOFTU=1  # No First Time User Experience.
    #export B2G_VALGRIND=1  # Enable Valgrind.
    EOF

.. _Changer les compilateurs par défaut:
    https://developer.mozilla.org/en-US/Firefox_OS/Customization_with_the_.userconfig_file#Changing_the_default_host_compiler

Configurer le build pour le Flame, et récupérer tous les fichiers (très long,
télécharge plus de 15Go de fichiers) ::

    ANDROIDFS_DIR=/home/mathieu/flame/backup-flame ./config.sh flame

.. note:: Ne pas oublier de remplacer */home/mathieu/flame/backup-flame* par le
          chemin absolu vers votre répertoire de sauvegarde du téléphone
          effectué à l'étape précédente.


Compiler
========

https://developer.mozilla.org/en-US/Firefox_OS/Building

Compiler (prend un peu moins d'une heure sur mon i7, en tournant sur les 4
cœurs en parallèle) ::

    ANDROIDFS_DIR=/home/mathieu/flame/backup-flame ./build.sh

.. note:: La taille totale utilisée par le répertoire *B2G* est de 22Go une
          fois la compilation terminée.


Installer sur le téléphone
==========================

https://developer.mozilla.org/en-US/Firefox_OS/Installing_on_a_mobile_device#Flashing_your_phone

..

    ./flash.sh


Mettre à jour
=============

À l'heure actuelle il n'y a pas de moyen public pour recevoir les mises à jours
automatiques sur le Firefox Flame, espérons que ça arrive vite ! En attendant,
voici une méthode manuelle très approximative (que j'espère pouvoir
améliorer) :

Mettre à jour le code ::

    git pull
    ./repo sync -d

Recompiler ::

    ANDROIDFS_DIR=/home/mathieu/flame/backup-flame ./build.sh

Mettre à jour tout sauf le module *user* qui écraserait toutes nos données
personnelles (mots de passe, applications installées, contacts...) ::

    ./flash.sh system boot gaia gecko data


Une autre méthode consiste à d'abord sauvegarder son profil ::

    adb pull /data/local local
    adb pull /data/b2g b2g

Puis, le restaurer une fois le *flash* effectué ::

    adb push local /data/local
    adb push b2g /data/b2g

D'après mes tests, au moins certaines données sont perdues avec cette méthode.
