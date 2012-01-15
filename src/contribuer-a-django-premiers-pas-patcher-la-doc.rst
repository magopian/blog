Contribuer à Django, premiers pas (patcher la doc) 
###################################################
:date: 2011-04-30 17:46
:category: django

Ceci est le troisième article dans la série, les premiers étant

#. `Contribuer à Django, premiers pas (revue de tickets)`_
#. `Contribuer à Django, premiers pas (les outils, l'environnement)`_

On sait donc quoi faire d'un ticket, et on a tous les outils en place
pour y répondre, c'est parti pour une contribution à la documentation !

Choisir son ticket
~~~~~~~~~~~~~~~~~~

Nous avons vu dans le `premier article`_ de la série qu'on peut trouver
les tickets soit sur la `page Reports de trac`_, soit sur le `super
dashbord`_ que Jacob Kaplan-Moss vient de créer.

Pour ma part, je me focalise pour le moment sur les tickets qui sont
*unreviewed* (non revus, qui viennent d'être créés).

N'oubliez pas qu'il est tout à fait possible, et même encouragé, de :

- ne pas s'occuper de tickets pour lesquels on ne se sent pas à la
  hauteur
- demander de l'aide sur le salon *#django-dev* sur le serveur irc
  *freenode*
- lancer des discussions pour avoir plus d'informations ou d'avis sur
  la liste de diffusion `*django-dev*`_

Nous allons, pour illustrer ce billet, examiner le ticket `#15886`_
dont le titre est "Improve django.core.serializers.get\_serializer()
docs".

Revendiquer le ticket
~~~~~~~~~~~~~~~~~~~~~

Comme indiqué dans la `doc sur la contribution`_, il est conseillé de
*claim* (revendiquer) un ticket avant de travailler dessus, pour éviter
de se retrouver à plusieurs sur le même ticket en parallèle, et sans le
savoir. Vu le nombre de contributeurs potentiels, il y a un risque que
quelqu'un d'autre soit déjà en train de travailler sur un patch.

Revendiquer le ticket se fait très simplement en sélectionnant
*accept*, tout en bas de la page de modification d'un ticket.

Il est par contre inutile de revendiquer un ticket pour les cas les
plus simples, ne nécessitant que quelques minutes de travail. Il suffit
alors de soumettre le patch directement, et c'est ce que j'ai fait pour
l'exemple choisi pour illustrer cet article.

Première étape : faire une revue du ticket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comme vous pouvez le constater, j'ai revu le ticket, et j'ai posté un
commentaire conseillant de créer un autre ticket séparé pour n'avoir
qu'un seul problème à résoudre dans celui-ci. Je n'ai pas changé l'état
du ticket, n'étant pas certain de ce qu'il fallait en faire.

Il faut noter que toute contribution (même un simple commentaire) peut
être utile et précieuse. Dans ce cas précis, il a servi à faire créer un
nouveau ticket, et à initier la discussion.

Dans ce cas particulier, Jacob a passé le ticket en *accepted*,
vraisemblablement parce qu'il ne restait pas d'objection : le problème
identifié dans le ticket (le manque de documentation) est maintenant
clairement séparé de la demande de nouvelle fonctionnalité, et le
"composant" concerné a bien été mis à jour.

Deuxième étape : proposer un patch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Et pour ça, rien de bien compliqué. Dans le `précédent article`_, nous
avons vu comment mettre en place un projet brouillon, et surtout comme
cloner le code source de Django, et compiler sa documentation.

Modifier la documentation
^^^^^^^^^^^^^^^^^^^^^^^^^

Pour cela, il faut déjà repérer la page concernée dans la documentation
de Django. Toujours en nous référant au ticket #15886 de l'exemple, un
gentil contributeur a déjà apporté un commentaire, et indiqué le lien
vers la page
`http://docs.djangoproject.com/en/1.3/topics/serialization/`_ (oui, ça
tombe bien, ce gentil contributeur, c'était moi ;)).

Si on inspecte l'url, on peut voir qu'il s'agit de la page
"serialization" dans la catégorie "topics". Le fichier correspondant,
dans le code source de Django, se trouve donc logiquement dans

::

    $ cd ~/projects/django/docs
    $ vi serialization.txt

Dans mon cas, j'utilise le `meilleur des éditeur`_, mais vous avez bien
entendu le choix des armes ;)

Une fois le bon endroit localisé pour apporter la clarification
demandée dans le ticket, il suffit de rajouter quelques lignes, en
utilisant son meilleur anglais.

Il est à ce propos fortement conseillé d'avoir au moins quelques
notions de `sphinx`_, l'outil utilisé pour générer la doc, et connaître
les ajouts apportés pour Django dans la page sur la `contribution à la
documentation`_.

Compiler la documentation
^^^^^^^^^^^^^^^^^^^^^^^^^

Nous l'avons vu dans le précédent article, il suffit pour celà
d'utiliser la commande suivante :

::

    $ make html

Si il y a le moindre problème de syntaxe *reStructuredText* vous le
verrez lors de l'exécution de cette commande. Il suffit alors de
consulter le résultat sur
`file:///chemin/vers/projects/django/docs/\_build/html/index.html`_.

Créer le patch
^^^^^^^^^^^^^^

Si vous avez suivi la méthode proposé dans le précédent article, vous
avez le cloné le miroir *git* de Django, et pouvez donc utilisez la
méthode ultra simple suivante :

#. créer une branche de développement pour y stocker les modifications à
   apporter : ``$ git checkout -b dev``
#. apporter les modifications nécessaires
#. *commit* les changements régulièrement, et retourner en 2. tant que
   c'est nécessaire : ``$ git commit -a -m "un message de commit"``
#. une fois fini, créer le patch :
   ``$ git diff master > nom_de_mon_patch.diff``

Il est très fortement recommandé de créer un patch avec l'extension
*.diff* pour qu'il soit correctement traité et affiché par *trac*, et de
l'attacher au ticket (au lieu de pointer vers un *diff* ou un *pull
request* sur github ou autre), pour simplifier au maximum la dure et
(déjà) fastidieuse tâche des *core developpers*.

Et surtout ne pas oublier de rajouter le flag "has patch" !

Pour reprendre notre exemple, vous pouvez `visualiser le patch final`_.

Attendre la validation de la communauté
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dans ce cas précis, j'étais inquiet de la dépendance qu'il pouvait y
avoir sur le ticket `#15889`_, qui est le ticket créé en parallèle pour
la demande d'ajout de fonctionnalité (renvoyer une exception spécifique
au lieu de *KeyError*). En effet, si le ticket #15889 était intégré dans
Django (avec la documentation associée), avant le ticket #15886, il
résulterait un problème de cohérence, avec deux parties de la même
documentation indiquant une levée d'exception différente.

J'ai donc soulevé la question sur le salon irc *#django-dev*, et la
réaction a été rapide : Alex a eu la gentillesse de répondre à mes
craintes en fermant le ticket comme étant un duplicat du ticket #15889.

Bah oui, mais mon patch alors ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Et là, j'ai envie de répondre : "*C'est le jeu, ma pov' Lucette*" !

Plus sérieusement, peu importe le temps passé (dans ce cas, vraiment
minime) sur un ticket, au final le but est de

- rendre Django meilleur
- apporter sa modeste contribution si nécessaire
- faciliter au maximum la tâche des *core devs*
- apprendre le plus possible au passage quand l'opportunité se présente

Astuce : se rajouter dans les destinataires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il suffit pour cela de cocher la case *add to cc* en bas du ticket, et
de sauvegarder. Si vous êtes enregistré et connecté, votre adresse mail
devrait être automatiquement ajoutée dans la liste des personnes qui
seront en copie du mail envoyé lors de chaque modification du ticket :
commentaire, changement d'état...

L'intérêt, en plus de recevoir les mails sur les tickets qui nous
concernent, est de pouvoir faire un filtre personnalisé pour `afficher
tous ces tickets`_.

Avec ce genre de requête personnalisée, il est beaucoup plus facile de
suivre l'évolution de "ses" tickets, et de pouvoir utiliser `l'offre
5-for-1`_ !

.. _Contribuer à Django, premiers pas (revue de tickets): ./contribuer-a-django-premiers-pas-revue-de-tickets.html
.. _Contribuer à Django, premiers pas (les outils, l'environnement): ./contribuer-a-django-premiers-pas-les-outils-lenvironnement.html
.. _premier article: ./contribuer-a-django-premiers-pas-revue-de-tickets.htm
.. _page Reports de trac: http://code.djangoproject.com/wiki/Reports
.. _super dashbord: http://dddash.ep.io/
.. _*django-dev*: http://groups.google.com/group/django-developers/
.. _#15886: http://code.djangoproject.com/ticket/15886
.. _doc sur la contribution: http://docs.djangoproject.com/en/dev/internals/contributing/#claiming-tickets
.. _précédent article: ./contribuer-a-django-premiers-pas-les-outils-lenvironnement.html
.. _`http://docs.djangoproject.com/en/1.3/topics/serialization/`: http://docs.djangoproject.com/en/1.3/topics/serialization/
.. _meilleur des éditeur: http://en.wikipedia.org/wiki/Editor_war
.. _sphinx: http://sphinx.pocoo.org/
.. _contribution à la documentation: https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/
.. _`file:///chemin/vers/projects/django/docs/\_build/html/index.html`: file:///chemin/vers/projects/django/docs/_build/html/index.html
.. _visualiser le patch final: http://code.djangoproject.com/attachment/ticket/15886/get_serializer_key_error_doc.diff
.. _#15889: http://code.djangoproject.com/ticket/15889
.. _afficher tous ces tickets: http://code.djangoproject.com/query?status=assigned&status=closed&status=new&status=reopened&cc=~mathieu.agopian&col=changetime&col=id&col=summary&col=status&col=owner&col=type&col=milestone&desc=1&order=changetime
.. _l'offre 5-for-1: http://groups.google.com/group/django-developers/browse_thread/thread/abc6cf0450812d82
