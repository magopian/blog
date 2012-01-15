Django : Envoyer des emails HTML avec images inline (intégrées)
###############################################################
:date: 2010-02-17 10:37
:category: django

Voyons comment envoyer des emails multiparties (texte et HTML) avec des
images *inline* (intégrées dans le mail lui-même, et non en pièce
jointe), et ceci en utilisant des templates afin de profiter (par
exemple) de l'i18n avec gettext, des filtres et tags, de l'utilisation
du contexte...

Ce code est un mélange de deux méthodes complémentaires, une sur les
`mails HTML par Ross Poulton`_, et l'autre venant d'un `djangosnippet
par sleytr`_.

Pour en faciliter l'utilisation et la maintenance, j'ai mis ce petit
module `django-nice-emails sur bitbucket`_.

Plutôt que de copier le code ici, je vais plutôt en décrire les grandes
étapes:

#. Utiliser le setting *DEFAULT\_FROM\_EMAIL* si l'expéditeur n'est pas
   fourni
#. Créer un *django.template.Context* à partir du dictionnaire fourni
   (permet de remplacer les *{{ var }}* dans les templates)
#. Utiliser le contexte créé pour initialiser le contenu texte, HTML
   ainsi que le sujet
#. Transformer le destinataire fourni en liste (si ce n'est pas déjà une
   liste de destinataires)
#. Créer un *django.core.mail.EmailMultiAlternatives* qui est la base de
   notre email (basé sur le contenu texte)
#. Rajouter la partie HTML
#. Rajouter les images en *inline* si nécéssaire
#. Envoyer le mai

Rien de compliqué donc dans ce code qui fait moins de 20 lignes
"utiles".

Voyons maintenant un exemple d'utilisation avec de la traduction et de
l'héritage de templates:

Les templates
~~~~~~~~~~~~~

On utilise ici la méthode de Ross Poulton qui consiste à ne fournir en
paramètre *template\_name* que la base du nom de fichier, sans
l'extension. On fournit ensuite au *django.template.loader* ce
*template\_name* avec l'extension *.txt* et *.html*, ces templates
doivent donc exister tous les deux.

**templates/test\_email.txt**

::

    {% load i18n %}
    {% trans "Bonjour" %} {{ nom }},

    {% blocktrans %}Ceci est un exemple de "nice-email" que je vous fait parvenir,
    à titre d'exemple, et bien que vous vous en fichiez{% endblocktrans %}.

    {% trans "Cordialement" %}

    Mathieu Agopian

**templates/test\_email.html**

::

    {% extends "base_email.html" %}
    {% load i18n %}
    {% block email_content %}
    <p>{% trans "Bonjour" %} {{ nom }},</p>
    <p>
        {% blocktrans %}Ceci est un exemple de "nice-email" que je vous fait parvenir,
        à titre d'exemple, et bien que vous vous en fichiez{% endblocktrans %}.
    </p>

    <p>{% trans "Cordialement" %}</p>

    <p><em>Mathieu Agopian</em></p>
    <img src="cid:signature" />
    {% endblock email_content %}

**templates/base\_email.html**

::

    <table width="600">
    <tr><td><img src="cid:logo" /></td></tr>
    <tr><td>
        {% block email_content %}{% endblock email_content %}
    </td></tr>
    </table>

Le contexte
~~~~~~~~~~~

Un simple dictionnaire python pour chaque tag utilisé dans les
templates:

::

    context = {'nom': 'Johnny Biboul'}

Les images
~~~~~~~~~~

Elles doivent être passées en paramètres dans un tuple de tuples, sous
la forme (('/chemin/vers/image.png', 'tagimage'),
'/chemin/vers/image2.png', 'tagimage2'), ...). Si les images sont dans
le répertoire *images* du *MEDIA\_ROOT*:

::

    images = (
        (path.join(settings.MEDIA_ROOT, 'images', 'signature.png'), 'signature'),
        (path.join(settings.MEDIA_ROOT, 'image', 'logo.png'), 'logo'))

Dans les templates, on utilisera les images sous la forme *<img
src='cid:tagimage' />*.

Le code
~~~~~~~

::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from os import path
    from django.conf import settings
    from django.utils.translation import ugettext
    from utils.nicemails import send_nice_email


    context = {'nom': 'Johnny Biboul'}
    images = (
        (path.join(settings.MEDIA_ROOT, 'images', 'signature.png'), 'signature'),
        (path.join(settings.MEDIA_ROOT, 'images', 'logo.png'), 'logo'))
    subject = ugettext(u"Test de mail pour %(nom)s") % {'nom': '{{ nom }}'}
    send_nice_email(template_name='test_email',
                    email_context=context,
                    subject=subject,
                    recipients='johnny@biboul.com',
                    sender='foo bar ',
                    images=images)

Conclusion
~~~~~~~~~~

Il vous suffit de mettre ce code dans une de vos vues pour pouvoir
faire de jolis mails de confirmation d'inscription, des newsletters, ou
voir même (bouh! c'est mal!) du mass-mailing. Veillez néanmoins à ne pas
forcer la dose sur le html, ou les images inlines!

.. _mails HTML par Ross Poulton: http://www.rossp.org/blog/2007/oct/25/easy-multi-part-e-mails-django/
.. _djangosnippet par sleytr: http://www.djangosnippets.org/snippets/285/
.. _django-nice-emails sur bitbucket: http://bitbucket.org/magopian/django-nice-emails/
