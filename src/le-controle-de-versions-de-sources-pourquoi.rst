Le contrôle de versions de sources: pourquoi?
#############################################
:date: 2009-03-30 19:07
:category: misc

Je vais vous raconter l'histoire de Brian. Brian est ingénieur
informaticien.

Le crash disque
~~~~~~~~~~~~~~~

Brian n'a pas de chance, et il a failli devoir pointer à l'ANPE quand
il s'est rendu compte que

#. Son disque dur avait crashé
#. Il n'avait pas fait de sauvegarde de son boulot

Heureusement, il a pu récuperer les sources sur le serveur de
production, et en moins de deux semaines il a pu réimplémenter les
dernières fonctionnalités et corrections de bugs qu'il avait apportées
au logiciel.

Le boss indécis
~~~~~~~~~~~~~~~

Brian n'a vraiment pas de chance, il a un boss indécis qui vient de lui
dire qu'il ne voulait finalement plus de la dernière fonctionnalité en
date:

"c'est une très mauvaise idée, commercialement parlant, supprime là au
plus vite".

Trois jours plus tard, Brian pense n'avoir oublié d'annuler les
modifications dans aucun fichier.

La faute à Murphy
~~~~~~~~~~~~~~~~~

Brian, qui a la poisse, se retrouve à débuguer un morceau de code
obscur, et se demande tout à coup qui a bien pu créer ce "code
spaghetti".

-  Serait-ce John, le cousin de l'oncle de sa soeur, qui code comme sa
   grand-mère?
-  Ou encore Steven, le surfer blond, qui sort juste de l'école et n'a
   jamais appris à commenter son code?

Si seulement Brian le savait, il pourrait demander des éclaircissement
à l'auteur, et aurait quelqu'un à pointer du doigt à son boss qui vient
de sortir son fouet.

Le CPOLD: la fausse solution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour reprendre le `blog de Roland`_, le CPOLD à d'innombrables
qualités:

-  pas de format de fichier complexe et susceptible de corruption
-  pas de conflits
-  aucun besoin d'un serveur dédié (on peut tout mettre ensemble, prod
   et dev confondues)
-  aucune limitation sur la gestion des branches
-  une rapidité insurpassable
-  une simplicité de mise en oeuvre et d'apprentissage enfantine
-  pas de modèle de développement imposé (centralisé, distribué, en
   quinconce, en hélice, toutes les variantes sont possibles)
-  des sauvegardes facilitées
-  etc...

Voici en quoi consiste la mise en place du CPOLD:

::

        $ cp fichier.py fichier.py.old

Et voici un exemple de mise en oeuvre du CPOLD:

::

        foo_dev
            foo.py
            foo.py.old
            foo.py.old.2009_03_29
            foo.py.marche_pas
            foo.py.todelete
            foo.py.OLD.2006_05_12
            foo.py.bak
            foo.py.fonctionalite_bar
            foo.py.bug
            foo.py.save.20081210
            foo.py.check
            foo.py.test

        foo_prod
            foo.py

        foo_savedev.tgz
        foo_save20090329_v2_0.tgz
        foo_save20080412_v1_2.tgz
        foo_save20060509_v1_0.tgz

Et pour faire bien, voici un extrait du fichier foo.py:

::

        ...
        def bar(thing): # Added the 10th of june, 2006 -- Steven
            """This function is very usefull!"""
            # Brian: refactored 20080410 for release 1.2
            #if thing == "bar": ### Steven: 11/06/06 fixed typo (was thing = "bar")
            #    return True;
            return (thing == "bar")
        ...

La fausse bonne idée
~~~~~~~~~~~~~~~~~~~~

Nous avons déjà vu les avantages du CPOLD, maintenant les
inconvénients:

-  Duplication de fichiers
-  Duplication de code
-  Réduction dramatique de la lisibilité
-  Difficulté de grouper des modifications (pour une fonctionnalité par
   exemple)
-  Ai-je déjà mentionné la duplication?

Conclusion
~~~~~~~~~~

Sommes-nous maintenant tous bien d'accord avec Brian pour dire que le
contrôle de versions, c'est indispensable? Et que le CPOLD, c'est
dépassé?

Dans une prochaine histoire, les enfants, nous verrons avec Brian quels
sont les merveilleux outils à notre disposition: les "Version Control
System" !

--------------

EDIT (05/06/2009): la totalité de cette article (cette première partie
ainsi que les deux suivantes, qui ne seront pas publiées sous forme de
billet) a été présentée à `PyCON.fr`_. Vous trouverez les liens vers la
présentation (en ligne, au format vidéo, et les sources) dans le billet
"`PyCON.fr: excellent!`_"

.. _blog de Roland: http://roland.entierement.nu/blog/2008/01/22/cpold-la-poudre-verte-du-suivi-de-versions.html
.. _PyCON.fr: http://pycon.fr
.. _`PyCON.fr: excellent!`: ./pyconfr-excellent.html
