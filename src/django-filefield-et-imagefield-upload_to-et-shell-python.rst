Django FileField et ImageField, upload_to et shell python
#########################################################
:date: 2009-02-19 19:30
:category: django

Le paramètre *upload\_to* des *FileField* et *ImageField*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le champ `upload\_to`_ permet d'indiquer où sauver un fichier de type
`django.core.files.File`_ par rapport au `MEDIA\_ROOT`_ spécifié
dans les settings.

Ce champ peut être une chaîne de caractères, ou un *callable*.

Chaîne de caractères pour upload\_to
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour notre example, prenons le modèle suivant:

::

    class MonModele(models.Model):
        fichier = models.FileField(upload_to="chemin")

Dans ce cas simple, tous les fichiers seronts sauvés dans le répertoire
*<MEDIA\_ROOT>/chemin/*.

Si on upload un fichier nommé *MonFichier.txt*, le chemin complet (sans
le *MEDIA\_ROOT*) sera *chemin/MonFichier.txt*.

Il est par ailleurs possible d'utiliser une syntaxe *strftime* comme
indiqué dans la `documentation du module time`_.

Pour stocker un fichier avec la date et l'heure:

::

    class MonModele(models.Model):
        fichier = models.FileField(upload_to="chemin/%Y%m%d_%H%M%S")

Et le résultat sera *chemin/2009-02-19\_18:40:03/MonFichier.txt*, ce
qui n'est pas vraiment ce à quoi on s'attendait.

En effet, cela créera un répertoire par fichier, au lieu de stocker la
date et l'heure dans le nom du fichier.

Pour arriver à nos fins, il nous faut utiliser une fonction pour le
calcul du chemin de stockage du fichier.

Fonction pour *upload\_to*
^^^^^^^^^^^^^^^^^^^^^^^^^^

Utiliser une fonction pour le calcul du chemin de stockage permet:

#. de modifier le nom du fichier lui-même, et pas seulement son
   répertoire de stockage
#. d'utiliser des informations spécifiques à l'instance du modèle pour
   lequel on stocke le fichier

Il nous faut par contre respecter les contraintes suivantes:

#. la fonction aura deux paramètres: *self*, l'instance, et *filename*,
   le nom du fichier uploadé
#. il n'est plus possible d'utiliser directement la syntaxe *strftime*

Voici le code qui va stocker un fichier avec la date et l'heure (et
prendra la date et l'heure automatiquement ajoutée au champ
*DateTimeField* avec le paramètre *auto\_add\_now*):

::

    class MonModele(models.Model):
        date = models.DateTimeField(auto_now_add=True)
        def upload_path(self, filename):
            return 'chemin/%s_%s' % (self.date.strftime("%Y%m%d_%H%M%S"), filename)
        fichier = models.FileField(upload_to=upload_path)

Ce coup-ci, on obtient bien un fichier
*chemin/2009-02-19\_18:40:03\_MonFichier.txt*, comme prévu.


Tester un modèle avec FileField dans l'interpréteur Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour pouvoir tester un modèle avec un FileField dans un intepréteur
Python (*python manage.py shell*), il y a quelques précautions à
prendre, comme commencer par "sauver" le *File*, comme indiqué sur la
`page suivante`_.

En effet, pour que le modèle soit correctement instancié, il faut:

#. créer une instance du modèle
#. la sauver (dans notre cas, afin que la date soit automatiquement
   stockée, et devienne accessible dans *upload\_path*)
#. ouvrir le fichier à "uploader"
#. créer un *django.core.files.File* à partir de ce fichier
#. sauver ce fichier pour pouvoir ensuite le tester

::

    >>> from mysite.models import *
    >>> mm = MonModele()
    >>> mm.save()
    >>> mm.date
    datetime.datetime(2009, 2, 19, 19, 4, 49, 538465)
    >>> from django.core.files import File
    >>> f = File(open("MonFichier.txt"))
    >>> mm.fichier.save(f.name, f, save=False)
    >>> mm.fichier
    <FieldFile: chemin/20090219_190449_settings.py>

Pour "sauver" le fichier, il faut fournir à la méthode *save* le nom du
fichier (*f.name*), le fichier lui-même (*f*), et un paramètre
spécifiant si on veut sauvegarder le fichier dans la base de donnée ou
pas.

Si nous ne voulions pas accéder à *date* qui est stockée
automatiquement, il aurait été inutile de sauvegarder l'instance de
MonModele (*mm*), et il aurait alors fallut remplacer le code de
*upload\_path* de la sorte

::

    def upload_path(self, filename):
        return 'chemin/%s_%s' % (self.date.strftime("%Y%m%d_%H%M%S"), filename)

par

::

    def upload_path(self, filename):
        import time
        return 'chemin/%s_%s' % (time.strftime("%Y%m%d_%H%M%S"), filename)

.. _upload\_to: http://docs.djangoproject.com/en/dev/ref/models/fields/#filefield
.. _django.core.files.File: http://docs.djangoproject.com/en/dev/topics/files/#the-file-object
.. _MEDIA\_ROOT: http://docs.djangoproject.com/en/dev/ref/settings/#media-root
.. _documentation du module time: http://docs.python.org/library/time.html#time.strftime
.. _page suivante: http://docs.djangoproject.com/en/dev/ref/files/file/#additional-methods-on-files-attached-to-objects
