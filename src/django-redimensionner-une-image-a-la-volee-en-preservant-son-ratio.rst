django: redimensionner une image à la volée en préservant son ratio
###################################################################
:date: 2011-02-16 13:15
:category: django

Une rapide recherche sur "django image thumbnail" vous sortira très
vraisemblablement de nombreuses solutions : snippets, applications,
astuces... en particulier la page `Thumbnails sur le wiki de django`_
qui liste beaucoup de solutions et leurs avantages.

Voulant faire simple, et profiter de toutes les améliorations que j'ai
pu trouver et compulser sur diverses solutions, voilà ma contribution.

Utiliser PIL et Image.thumbnail()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python Image Library est une des (la?) solutions les plus avancées sur
le traitement d'image en python. Dans mon cas pratique, je veux, lors
d'un upload d'une photo, pouvoir :

#. redimensionner la photo, pour qu'elle fasse **au maximum** 800x600 :
   elle sera affichée avec un max-width et un max-height
#. créer un thumbnail
#. stocker les images au format jpg
#. tout ceci sans au préalable sauver l'image sur le disque

Beaucoup des solutions que j'ai pu trouver utilisaient la fonction
*resize()* de PIL.Image, et utilisaient un calcul du ratio pour
conserver l'aspect de l'image. Heureusement, PIL a pensé au fainéant que
je suis, et fournit la fonction *thumbnail()* qui va automatiquement
redimensionner l'image pour qu'elle rentre dans les dimensions maximales
qu'on lui fournit.

Le modèle
~~~~~~~~~

Modèle très simple pour illustrer notre propos :

::

    class Foo(models.Model):
        photo = models.ImageField(upload_to='photos/')
        thumbnail = models.ImageField(upload_to='photos/thumbs/')
        legend = models.CharField(max_length=50)

La solution
~~~~~~~~~~~

Cette solution est largement inspirée de cet article qui collait le
plus à la version que je souhaitais obtenir au final : `generate
thumbnails in django with PIL`_.

Tout d'abord le morceau de code qui récupère l'image en mémoire
(stockée dans un *InMemoryUploadedFile*) et la converti en mode *RGB* si
nécessaire :

::

    from PIL import Image
    from cStringIO import StringIO
    from django.core.files.uploadedfile import SimpleUploadedFile

    ...

        def save(self, *args, **kwargs):
            if has_changed(self, 'photo'):
                # on va convertir l'image en jpg
                filename = path.splitext(path.split(self.photo.name)[-1])[0]
                filename = "%s.jpg" % filename

                image = Image.open(self.photo.file)

                if image.mode not in ('L', 'RGB'):
                    image = image.convert('RGB')

                # d'abord la photo elle-même
                self.photo.save(
                        filename,
                        create_thumb(image, settings.IMAGE_MAX_SIZE),
                        save=False)

                # puis le thumbnail
                self.thumbnail.save(
                        '_%s' % filename,
                        create_thumb(image, settings.THUMB_MAX_SIZE),
                        save=False)

Et enfin la fonction *create\_thumb* qui prends en paramètre une
PIL.Image et une taille du style *(800, 600)* :

::

    def create_thumb(image, size):
        """Returns the image resized to fit inside a box of the given size"""
        image.thumbnail(size, Image.ANTIALIAS)
        temp = StringIO()
        image.save(temp, 'jpeg')
        temp.seek(0)
        return SimpleUploadedFile('temp', temp.read())

Retourner un *SimpleUploadedFile* permet de le fournir directement au
*save()* de l'*ImageField*.

Le bonus
~~~~~~~~

Vous avez sûrement remarqué la fonction *has\_changed()* dans l'appel
de la méthode *save()* ci-dessus... en effet, il serait peu utile, voire
même carrément indésirable de générer une nouvelle version de la photo
et de son thumbnail à chaque fois que notre modèle est sauvé!

On se retrouverait vite avec autant de photos et de thumbnails que le
nombre de fois qu'on a sauvé notre modèle, même si la seule modification
portait sur la légende.

Pour limiter ça, on ne redimensionne et génère le thumbnail que si la
photo a été modifiée, ce qu'on teste avec la fonction suivante :

::

    def has_changed(instance, field, manager='objects'):
        """Returns true if a field has changed in a model 

        May be used in a model.save() method.

        """
        if not instance.pk:
            return True
        manager = getattr(instance.__class__, manager)
        old = getattr(manager.get(pk=instance.pk), field)
        return not getattr(instance, field) == old

.. _Thumbnails sur le wiki de django: http://code.djangoproject.com/wiki/ThumbNails
.. _generate thumbnails in django with PIL: http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
