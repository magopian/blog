Installer PIL (Python Imaging Library) facilement avec pip
##########################################################
:date: 2010-02-09 12:41
:category: django


Le fabuleux utilitaire *pip* de `Ian Bicking`_ est un remplacement à
*easy\_install* qui fonctionne très bien avec *virtualenv* (pas
étonnant, c'est du même auteur!).

Je laisse le soin au lecteur de consulter la documentation sur ces deux
utilitaires très pratiques et indispensables à tout développeur python.

Voici la commande à utiliser pour installer PIL (Python Imaging
Library) dans votre environnement virtuel:

::

    $ pip -E /path/to/venv install http://effbot.org/downloads/Imaging-1.1.7.tar.gz

Vous pouvez consulter la liste des versions disponibles en vous rendant
sur la page officielle de `Python Imaging Library`_.

ATTENTION: Il faut avoir les sources de python installées et
disponibles afin de pouvoir compiler le paquet. Sur debian, il vous
suffit de taper

::

    $ aptitude install python-dev

Si vous avez une erreur pip du genre

::

    ImportError: No module named pkg_resources

il vous faut aussi installer python-pkg-resources:

::

    $ aptitude install python-pkg-resources

.. _Ian Bicking: http://ianbicking.appspot.com/
.. _Python Imaging Library: http://www.pythonware.com/products/pil/
