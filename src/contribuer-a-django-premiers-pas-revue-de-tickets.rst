Contribuer à Django, premiers pas (revue de tickets)
####################################################
:date: 2011-04-24 17:41
:category: django

Contribuer au framework web Django... tout un programme, et très
effrayant de prime abord. Depuis des années que j'utilise le framework,
je commence tout juste à y contribuer, et je peux vous assurer que
jusqu'à hier encore, je ne pensais pas être à la hauteur.

Or, ce qu'il y a de génial, c'est que tout le monde est à la hauteur,
et que chacun peut apporter sa pierre à l'édifice ! La contribution la
plus simple consiste à faire la revue de nouveau tickets, et c'est très
utile : si vous ne me croyez pas, regardez ce qu'il est écrit :

-  `Jacob Kaplan-Moss (Django BDFL) sur la mailing list django-dev`_ :
   "this is totally something anyone here can do"
-  `Documentation officielle Django page "contributing"`_ : "there’s a
   lot that general community members can do to help the triage process"
-  `Documentation officielle de Django page "how contribue"`_ : "Django
   is a community project, and every contribution helps. We can’t do
   this without YOU!"

Le cheminement logique et officiel pour devenir un contributeur Django
est :

#. être motivé pour donner un peu de temps en retour à la communauté qui
   a fait un framework qui me fait vivre !
#. se créer un compte sur le `trac de Django`_
#. lire dans l'ordre (ou le désordre) les pages suivantes

   -  `comment contribuer`_
   -  `référence sur la contribution`_
   -  `FAQ`_
   -  `comment contribuer de la doc`_

Une fois qu'on a lu tout ça, on est prêts à choisir des tickets, soit
sur la `page Reports de trac`_, soit sur le `super dashbord`_ que Jacob
Kaplan-Moss vient de créer.

Mais c'est trop long de tout lire !
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Effectivement, il y a beaucoup de ressources, et toutes ne sont pas
indispensables pour démarrer.

Pour vraiment débuter, je pense qu'il est indispensable de lire le
premier document sur `comment contribuer`_ qui a l'avantage d'être assez
concis. Il faut ensuite comprendre les différentes étapes d'un ticket,
qui sont indiquées sur le deuxième document, dans la section `Ticket
Triage`_, avec une image très claire.

Mais c'est trop compliqué, je suis pas assez expérimenté en Django !
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il n'est pas nécessaire d'être un expert pour pouvoir faire de la revue
de tickets. Si vous voyez un ticket que vous pensez pouvoir traiter,
faites-le, sinon passez au suivant!

Les tickets qui sont en état *unreviewed* peuvent être fermés, acceptés
ou passés en "besoin d'une décision de design" :

Ticket fermé, avec les statuts suivants :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **invalid** si ce n'est ni un bug, ni une demande d'amélioration,
   mais une question de support ou sur autre chose que django
#. **duplicate** si le même bug ou demande d'amélioration a déjà été
   signalé. Pour le savoir, il suffit de faire une recherche dans la
   liste des tickets, puis de fermer le ticket en cours en indiquant que
   c'est un duplicat du ticket #xxxx
#. **worksforme** si vous avez pu tester que ça marche pour vous, avec
   les informations fournies par le créateur du ticket
#. **needsinfo** si il manque des informations pour pouvoir reproduire
   le bug, mais que le bug a l'air d'être réel

Les autres statuts (**fixed** et **wontfix**) ne concernent que les
*core developers*.

Dans tous les cas, lors de la fermeture d'un ticket, il est primordial
de rester poli et agréable, en signalant le problème au créateur du
ticket, et lui indiquant qu'il peut rouvrir le ticket si il fournit plus
d'informations, si on a mal compris le problème...

Il faut garder à l'esprit que le créateur a lui aussi passé du temps
pour signaler le problème, et qu'il lui a fallut de la motivation pour
faire la démarche de créer ce ticket !

Ticket accepté, avec les indications suivantes :
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. **has patch** dans le cas où un patch est fourni (documentation ou
   code)
#. **needs documentation** si il y a un patch pour une fonctionnalité,
   mais qu'il n'y a pas la documentation qui doit aller avec
#. **needs tests** si il y a un patch pour une fonctionnalité sans les
   tests unitaires nécessaires, ou un patch correctif sans les tests de
   non régression
#. **patch needs improvement** si le patch de documentation n'est pas
   assez clair ou si le correctif n'est pas acceptable tel quel
   (possibilité d'améliorations, conformité aux conventions de
   codage...)
#. **easy pickings** pour indiquer que ce ticket peut être facilement et
   rapidement réglé, même par un débutant (apparaîtra dans une `liste personnalisée`_ accessible sur la `page report de trac`_)

Ticket passé en "design decision needed"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

C'est le cas notamment des tickets qui proposent des améliorations du
framework, ou des corrections de "bug" qui n'en sont pas forcément, ou
qui pourraient avoir plusieurs corrections possibles. Une fois le ticket
passé en *DDN*, un des *core developers* pourra le passer en **wontfix**
ou en **accepted**.

Et je peux changer le statut de mes propres tickets alors ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Non.

Pour une réponse plus longue : il vaut toujours mieux au moins une
validation externe pour être sûr qu'on a pas oublié quelque chose, ou
mal compris la doc, ou fait une typo, ou ...

Trop long, j'ai pas lu
~~~~~~~~~~~~~~~~~~~~~~

C'est bien dommage. Il faut tout de même un minimum de motivation pour
rendre un peu à la communauté de ce qu'elle nous apporte.

J'ai lu, mais tu veux bien résumer ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour débuter et commencer à contribuer, il est très facile de faire de
la revue de tickets, c'est-à-dire relire et (in)valider des tickets qui
viennent d'être créés.

Dans certains cas, la validation (ou fermeture) du ticket ne
nécessitera même pas de test ou de reproduction. Pour les autres, il
vaut mieux lire le reste des documents que j'ai listés en début de cet
article, ou attendre que je fasse un résumé dans un prochain billet !

Le cadeau bonux
~~~~~~~~~~~~~~~

Jacob Kaplan-Moss a lancé `une idée`_ pour motiver les revues de
tickets : 5 tickets revus, un ticket revu par un des *core developers*
participant à l'opération (Jacob Kaplan-Moss, Alex Gaynor et Carl
Meyer).

Donc si vous avez un ticket que vous aimeriez qu'un des *core dev*
considère, vous savez ce qu'il vous reste à faire !

Dans le prochain article, nous verrons `comment mettre en place son
environnement`_ pour pouvoir contribuer sans douleur !

.. _Jacob Kaplan-Moss (Django BDFL) sur la mailing list django-dev: http://groups.google.com/group/django-developers/browse_thread/thread/abc6cf0450812d82
.. _Documentation officielle Django page "contributing": http://docs.djangoproject.com/en/dev/internals/contributing/#triage-by-the-general-community
.. _Documentation officielle de Django page "how contribue": http://docs.djangoproject.com/en/dev/howto/contribute/#the-spirit-of-contributing
.. _trac de Django: http://www.djangoproject.com/accounts/register/
.. _comment contribuer: http://docs.djangoproject.com/en/dev/howto/contribute/
.. _référence sur la contribution: http://docs.djangoproject.com/en/dev/internals/contributing/
.. _FAQ: http://docs.djangoproject.com/en/1.3/faq/contributing/
.. _comment contribuer de la doc: http://docs.djangoproject.com/en/dev/internals/documentation/
.. _page Reports de trac: http://code.djangoproject.com/wiki/Reports
.. _super dashbord: http://dddash.ep.io
.. _Ticket Triage: http://docs.djangoproject.com/en/dev/internals/contributing/#ticket-triage
.. _liste personnalisée: http://code.djangoproject.com/query?status=!closed&easy=1&stage=Accepted&order=priority
.. _page report de trac: http://code.djangoproject.com/wiki/Reports
.. _une idée: http://groups.google.com/group/django-developers/browse_thread/thread/abc6cf0450812d82
.. _comment mettre en place son environnement: ./contribuer-a-django-premiers-pas-les-outils-lenvironnement.html
