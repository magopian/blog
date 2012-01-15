La bidouille django du jour: appeller un templatetag depuis un autre templatetag
################################################################################
:date: 2011-05-11 11:59
:category: django

Cet article n'est pas écrit par Mathieu. Enfin si, mais par `un autre Mathieu`_, qui n'a pas de blog en ce moment et abuse^Wprofite
de la gentillesse du maître de ces lieux pour poster ici.

Introduction
~~~~~~~~~~~~

Avez vous toujours rêvé d'appeler un templatetag Django depuis un autre
templatetag ? Allez, avouez-le : dans vos rêves les plus fous, vous
aimeriez pouvoir faire:

::

    @register.simple_tag
    def my_templatetag():
        if condition:
            return tag1()
        else:
            return tag2()

Ça marchera si vos tag1 et tag2 sont des simple\_tags, vu que c'est
directement une chaîne de caractères qui est retournée. Là où ça
commence à se compliquer, c'est si vous voulez que ça marche avec
n'importe quel templatetag, et notamment les inclusion\_tags. En effet,
en appelant un inclusion\_tag "à la main", vous vous retrouvez avec
juste le dictionnaire qu'il retourne comme contexte, au lieu d'avoir le
"vrai" résultat.

Zut, mais comment faire alors ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour comprendre comment faire pour contourner ce problème, il faut
regarder comment un templatetag fonctionne. Quand vous déclarez un
inclusion\_tag ou un tag classique, que se passe-t-il ?

#. Tout d'abord, via le décorateur ``@register.tag`` ou
   ``@register.inclusion_tag``, votre templatetag est enregistré dans la
   variable register, que vous avez dû déclarer de la sorte:
   ``register = Library()``.
#. Si on inspecte cette fameuse ``Library``, on se rend compte que
   chaque tag s'enregistre dans un dictionnaire, dans l'attribut tags.
   Ce dictionnaire contient la fonction permettant de générer l'instance
   de ``Node`` correspondant à votre tag. Dans le cas d'un
   inclusion\_tag, il y a un peu de complexité qui vous est planquée, vu
   que, contrairement à l'enregistrement d'un tag "classique" via
   ``@register.tag``, vous ne déclarez pas de sous-classe de ``Node``,
   et vous ne jouez pas non plus avec un parser de tokens.
#. Au moment où le template rencontre votre templatetag, il récupère la
   fonction à appeler dans l'instance de Library qui va bien, et
   instancie le ``Node`` avec ``parser`` (l'instance du ``Parser``) et
   ``token`` (l'instance de ``Token`` correspondant à tout ce qui était
   entre {% et %})
#. Ensuite, au moment d'afficher votre template, la méthode ``render()``
   de chaque ``Node`` est appelée. Celle-ci reçoit notamment le contexte
   courant.

Du coup, la grosse bidouille consiste simplement à faire la même chose
que Django fait. Ça donne ça:

::

    @register.tag
    def my_templatetag(parser, token):
        # On suppose que vous êtes dans le même module, sinon il faut aller chercher le register
        # qui va bien dans un autre module python
        if condition:
            return register.tags['tag1'](parser, token)
        else:
            return register.tags['tag2'](parser, token)

La beauté du truc, c'est que vous enregistrez un tag normal, mais quand
il est appelé, il utilise une autre instance de ``Node``, qui provient
d'un de ses copains.

Gestion des paramètres
----------------------

Il reste cependant un écueil : comment gérer les paramètres ? C'est en
fait très facile: il faut modifier le ``token`` qu'on passe pour tromper
Django. Et c'est là où la bidouille est un peu crade, vous devez faire
comme si on appelait le templatetag depuis le template:

::

    @register.tag
    def my_templatetag(parser, token):
        # On suppose que vous êtes dans le même module, sinon il faut aller chercher le register
        # qui va bien dans un autre module python
        if condition:
            token.contents = 'tag1 argument1 argument2'
            return register.tags['tag1'](parser, token)
        else:
            token.contents = 'tag2 argument1 argument2 argument3'
            return register.tags['tag2'](parser, token)

Conclusion
----------

Et voilà ! Je vous conseille, si vous utilisez cette technique, même si
vous n'avez pas besoin d'arguments, de toujours modifier
``token.contents``, histoire d'être sûr.

On peut encore pousser le vice plus loin et gérer des paramètres dans
notre templatetag 'parent', mais ça suffit pour aujourd'hui :)

.. _un autre Mathieu: http://virgule.net/
