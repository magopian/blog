Vim, Restructured Text et espaces insécables
############################################
:date: 2012-03-14 12:07
:category: misc


Pour avoir un espace insécable dans un fichier HTML généré à partir d'un fichier ReST, il suffit d'utiliser un espace insécable (unicode ``\xA0``) dans le fichier source. Il sera alors automatiquement converti en ``&nbsp;`` lors de la compilation en HTML.

Pour entrer un espace insécable avec vim il faut faire la combinaison de touches suivantes : ``CTRL+k N S`` (si on a une touche *Compose* c'est ``Compose <space> <space>``).
Sur certains claviers (mac, bepo...) c'est plus simple : ``CTRL+space`` ou ``ALTGR+space``.

Étant fainéant, voici comment j'ai mappé cette combinaison barbare sur CTRL+space :

.. code-block:: vim

    " map CTRL+k S N (non-breaking space) to CTRL+space
    imap <Nul> <C-k>NS

Attention, si vous utilisez *gvim*, il vous faut remplacer ``<Nul>`` par  ``<C-space>``.

Enfin voici une solution simple et rapide pour visualiser les espaces insécables (et les espaces en fin de ligne) :

.. code-block:: vim

    " visual indication of trailing and non-breaking spaces
    set listchars=trail:-,nbsp:_
    set list


La commande barbare
~~~~~~~~~~~~~~~~~~~

Pour ceux qui comme moi oublient régulièrement des espaces insécables, voici comment remplacer tous les espaces avant un ``:``, ``;``, ``?`` ou ``!`` (bien remplacer ``<CTRL+k N S>`` par la séquence de touches pour générer l'espace insécable) :

.. code-block:: vim

    :%s/\(\S\) \([:;?!]\)/\1<CTRL+k N S>\2/g

Je vous avais prévenus, c'est violent. En gros, ce que ça fait :

* ``:%s/<search>/<replace>/g`` : faire une recherche et un remplacement sur tout le fichier (et remplace toutes les occurences sur une même ligne)
* ``\(\S\) \([:;?!]\)`` : le pattern à chercher. Ça donne ``(\S) ([:;?!])`` sans l'échappement : trouver tous les espaces entre un *non-espace* et une ponctuation, en capturant le *non-espace* ainsi que la ponctuation
* ``\1<CTRL+k N S>\2`` : ce par quoi il faut remplacer. ``\1`` et ``\2`` sont les deux morceaux capturés à l'étape de recherche, donc le *non-espace* et la ponctuation respectivement.

Avec tout ça, plus d'excuses pour ne pas utiliser des espaces insécables quand c'est nécessaire (merci `@n1k0 <https://twitter.com/n1k0>`_ pour la piqûre de rappel ;).
