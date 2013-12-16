Objets ou fonctions
###################
:date: 2013-12-16 13:39
:category: misc


Objets ou fonctions ? Voilà une question que je ne me pose pas assez souvent.

De part mon utilisation d'un langage objet (Python_), et d'un framework web
(Django_) basé sur des objets (utilisation d'un ORM_, de `vues génériques`_
sous forme de classes), je ne me pose quasiment jamais la question : j'utilise
par défaut des objets.

.. _Python: http://python.org
.. _Django: https://djangoproject.com
.. _ORM: https://docs.djangoproject.com/en/dev/topics/db/
.. _vues génériques:
    https://docs.djangoproject.com/en/dev/topics/class-based-views/

Seulement, depuis mes explorations du côté de langages fonctionnels (Clojure_,
Erlang_ et Elixir_), je me rends compte que la question mérite vraiment d'être
posée.

.. _Clojure: http://clojure.org
.. _Erlang: http://erlang.org/
.. _Elixir: http://elixir-lang.org/


Un exemple concret
==================

Pour le reste de cet article, je vais me baser sur l'exemple concret du `jeu de
la vie de Conway`_ qui était le sujet de la `journée de code retreat à
Marseille`_ à laquelle j'ai assisté ce samedi 14 Décembre.

.. _jeu de la vie de Conway: http://fr.wikipedia.org/wiki/Jeu_de_la_vie
.. _journée de code retreat à Marseille:
    http://gdcr13.coderetreat-marseille.org/

Voici deux implémentations, avec des objets puis avec des fonctions, pour
étayer le discours. Je ne prétends pas fournir le code parfait, mais uniquement
un support de discussion.

J'ai essayé de reprendre le même code (parcours de la grille, recherche des
cellules voisines, calcul de la vie ou mort de la cellule) lorsque c'était
possible pour avoir le plus de points de comparaison possibles.


Avec des objets
---------------

J'ai opté pour un découpage « raisonnable » (on a fait une session avec un
``CellContext`` qui s'occupait de gérer les cellules voisines, au lieu de
grouper ça directement dans l'objet ``Cell``, mais je trouvais ça un brin trop
*over-engineered*).

La logique est d'initialiser une fois pour toutes les cellules voisines pour
chaque cellule, ce qui simplifie le comptage des voisines en vie.

.. include:: includes/gol_objects.py
    :code: python

**67 lignes, 2 objets, 9 méthodes.**


Avec des fonctions
------------------

.. include:: includes/gol_functions.py
    :code: python

**43 lignes, 4 fonctions.**


Le rôle des données
===================

Avec des objets
---------------

En :abbr:`POO (Programmation Orientée Objet)`, on scinde la donnée d'entrée
(base de données, fichiers, flux de données...) pour la répartir dans
différents objets. Dans notre exemple, un objet ``World`` qui stocke l'ensemble
des cellules, et un objet ``Cell`` qui stocke son état (en vie ou morte) et
l'ensemble de ses voisines.

* **+** Représentation mentale aisée des différentes entitées
* **+** Répartition des responsabilités
* **-** Verbosité
* **-** Difficulté pour les tests : il faut gérer les
  :abbr:`fixtures (données pour l'initialisation des objets)`


Avec des fonctions
------------------

En fonctionnel, on traite directement la donnée d'entrée par des étapes
successives et différentes fonctions que l'on compose.

* **+** Concision
* **+** Moins de code à maintenir, moins de code à lire et comprendre
* **+** Facilité pour les tests
* **-** Duplication de la donnée (nouveau monde à chaque itération)
* **-** Recalcul des voisins à chaque itération


La réutilisation du code
========================

Dans notre exemple très basique, pas de réutilisation du code. Pas d'héritage
pour les objets, pas de composition de fonctions.


Avec des objets
---------------

La réutilisation du code dans la POO se fait principalement par l'héritage
d'objets.

Imaginons que nous ayons demain un monde différent, qui au lieu d'être
représenté par un tableau de cellules carrées, soit un amas de cellules
hexagonales. On pourrait alors avoir un objet ``HexagonalWorld`` qui hériterait
de ``World`` et redéfinirait les méthodes ``__init__`` et ``__str__``.

Le reste du code resterait le même, et serait donc réutilisé.

On peut encore imaginer des cellules plus ou moins résistantes qui, en
redéfinissant ``mutate`` auraient des règles différentes de vie ou de mort.


Avec des fonctions
------------------

La réutilisation du code dans la programmation fonctionnelle se fait par la
composition de fonctions.

On aurait pu imaginer partir d'un format différent pour le monde, sous la forme
d'une suite de ``0`` et de ``1``.

On aurait alors tout d'abord transformé chaque ``0`` ou ``1`` en booléen puis
découpé cette suite en lignes d'une longueur donnée, composant deux fonctions :

::

    data = "001001100"
    to_bool(data) == [False, False, True, False, False, True, True, False, False]
    to_grid(to_bool(data)) == [
        [False, False, True],
        [False, False, True],
        [True, False, False]]

Si ce n'est pas d'une série de ``0`` et de ``1`` qu'on part, mais de ``X`` et
de ``O``, on change la fonction ``to_bool``, la fonction ``to_grid`` reste
identique.


La gestion de l'état
====================

Voilà le plus gros point d'achoppement à mon avis, la plus grosse différence
entre les langages fonctionnels (plus ou moins purs) et les langages objets :
la gestion et le stockage d'un état changeant et les effets de bord.

En programmation fonctionnelle, il n'y a pas de stockage d'un état changeant
dans les fonctions.  Une fonction retournera **toujours** le même résultat pour
la même donnée en entrée.

Une méthode d'un objet par contre pourra retourner un résultat différent selon
l'état stocké dans l'objet. Une méthode ``is_alive`` sur un objet ``Cell``
retournera ``True`` ou ``False`` selon l'état de la cellule.

L'avantage d'avoir un état changeant est de pouvoir justement cantonner des
morceaux de données dans différents objets, chacun avec ses responsabilités,
son domaine d'application. Avec un objet donné, on a toutes les informations
nécessaires à la gestion de cet objet, et on peut connaître à tout instant son
état actuel.

Le stockage de l'état va souvent de pair avec les effets de bord. Une méthode
``set_alive`` sur un objet ``Cell`` va par exemple passer cette cellule
vivante, mais aussi incrémenter son âge, ou encore incrémenter le compteur du
nombre de cellules vivantes de l'objet ``World``.

Les inconvénients sont nombreux :

* les fixtures nécessaires pour l'écriture de tests (il faut toujours gérer
  l'initialisation des objets dans un état connu)
* les effets de bord : pas toujours connus, pas faciles à prévoir sans avoir
  une connaissance parfaite de l'objet et du code
* une programmation concurrentielle très complexe : il faut que chaque
  *process* soit au courant de l'état, qui doit donc être partagé/géré, ainsi
  que les effets de bord


Est-ce qu'on s'est trompés ?
============================

Il est communément admis (en tout cas dans mon entourage) que l'utilisation
d'objets est plus intuitive, plus facile, plus claire et explicite. Seulement,
lors de la *code retreat* et des différentes sessions, j'ai été confronté à des
visions très différentes de mes collègues de *pair-programming*, par exemple
sur le découpage des objets, ou sur leur responsabilité :

* est-ce qu'il faut un objet ``CellContext`` qui gère le contexte de la
  cellule, ses voisines
* est-ce la responsabilité de la cellule de décider si elle doit vivre ou
  mourir, ou plutôt celle du monde (ou de l'organisme, selon comment on
  l'appelle) ? Comment gérer le cas de cellules prédatrices qui tueraient
  d'autres cellules (ce n'est plus alors à la cellule elle-même de décider si
  elle doit mourir).
* plus de code a écrire prends plus de temps, et pour des sessions de 45
  minutes c'est très court, surtout en mode TDD (et on a vu que c'était plus
  difficile et long d'écrire des tests pour des objets : dans mon cas, 118
  lignes de tests)

L'impression que ça m'a laissé est qu'avoir utilisé des objets nous mettait une
contrainte supplémentaire, un frein dont on aurait pu se passer.

Alors oui, il y a de meilleures manières d'aboutir au même résultat. Oui, cet
exemple trivial n'est que peu représentatif de notre métier de développeur qui
est de se frotter à des problèmes beaucoup plus complexes.

Oui, si il y a autant de monde qui fait de la POO, c'est vraisemblablement que
le concept n'est pas aberrant. Mais attention à la loi des nombres, ce n'est
pas parce que Java et PHP sont les langages les plus courants que je vais me
mettre à en (re)faire.

Mais plus j'y pense, et plus je me dis qu'on s'est peut-être trompés. Pour les
curieux (et je vous recommande très fortement d'être curieux !), voici quelques
liens à voir absolument :

* ce qu'aurait pu (dû ?) être la programmation : `The future of programming`_
  de Bret victor
* la programmation concurrentielle, on a plus le choix : `Erlang software for a
  concurrent world`_ de Joe Armstrong (créateur de Erlang)
* la simplicité dans la programmation : `Simple made easy`_ de Rich Hickey
  (créateur de Clojure)
* pourquoi la programmation fonctionnelle : `Why functional programming matters`_ de John Hughes (impliqué dans la création de Haskell)
* comment battre la concurrence avec Lisp : `Beating the averages`_ de Paul
  Graham (entrepreneur et capital risque)

.. _The future of programming: http://worrydream.com/dbx/
.. _Erlang software for a concurrent world:
    http://www.infoq.com/presentations/erlang-software-for-a-concurrent-world
.. _Simple made easy:
    http://www.infoq.com/presentations/Simple-Made-Easy-QCon-London-2012
.. _Why functional programming matters:
    http://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf
.. _Beating the averages: http://www.paulgraham.com/avg.html
