Latence et boucle de rétroaction
################################
:date: 2014-07-14 13:56
:category: misc


Latence
=======

La latence_ en informatique est un délai minimum de transmission. C'est un des
principaux ennemis de la performance notamment dans le domaine du web.

.. _latence: http://fr.wikipedia.org/wiki/Latence_%28informatique%29

Un site web est généralement composé de multiples fichiers statiques (css,
javascript, images et icônes en tout genre). Pour afficher la totalité d'une
page, il faut donc faire de multiples requêtes au serveur, chacune prenant un
certain temps de traitement, à quoi on rajoute la latence (le temps de
transfert sur le réseau).

On imagine facilement l'impact d'une forte latence lorsqu'il faut effectuer
plusieurs dizaines voire centaines de requêtes. Même si la latence n'est que de
10ms, si on multiple ça par 100, on atteint déjà une seconde.

Prenons un autre exemple : il n'est pas rare d'avoir des pages nécessitant des
dizaines (des centaines, voire des milliers ?) de requêtes SQL à une base de
donnée. Là encore, il faut multiplier ce nombre de requête par le temps de
traitement par la base de donnée, mais aussi par la latence.

Étant donné la difficulté de réduire la latence, l'optimisation de la
performance passe par le réduction du nombre de requêtes : on fait des
*bundles* pour les fichiers statiques (on regroupe toutes les CSS ou les
fichiers javascript, on crée des *image map* pour les icônes), on fait usage du
*JOIN* pour les requêtes SQL...


Boucle de rétroaction
=====================

La `boucle de rétroaction`_ (appelée « feedback loop » en anglais) permet de
raffiner un système afin d'arriver à un équilibre, à un objectif.

.. _boucle de rétroaction:
    http://fr.wikipedia.org/wiki/Boucle_de_r%C3%A9troaction

Une boucle de rétroaction basée sur des mesures de position permettra à robot
d'atteindre la position souhaitée : la vitesse et la direction seront adaptées
en fonction de la distance à l'objectif.

Plus la boucle de rétroaction sera longue, plus l'équilibre sera long a
atteindre. En effet, si la mesure de position ne se fait qu'une fois toutes les
10 secondes, soit le robot devra se déplacer très lentement, soit faire de
nombreux aller-retours.


Le rapport ?
============

En tant qu'informaticien, il nous arrive régulièrement d'avoir à raffiner un
bout de code en fonction de différents paramètres : l'expression du besoin, la
rapidité d'exécution, l'occupation mémoire...

Et ce raffinage se fait par le biais d'une boucle de rétroaction qui peut
prendre différentes formes :

- des tests automatisés (test unitaires ou fonctionnels, TDD...)
- des tests manuels
- des simulations
- des aller-retours avec l'utilisateur final, le décideur, ...

Si la latence s'invite dans ce mécanisme, on se retrouve dans la même situation
que le robot qui doit atteindre une position, mais qui n'a de retour sur sa
position que rarement. Soit on avance vite et on risque les aller-retours
(comprendre : réécriture du code), soit on avance lentement.

Dans tous les cas, c'est un cauchemar.

Voici quelques exemples de latence :

- besoin mal exprimé ou mal compris (la mesure de position n'est pas fiable)
- périmètre fonctionnel qui change (la position finale du robot change en cours
  de route)
- grand nombre d'aller-retours avec l'utilisateur final/décideur (nécessité de
  faire un très grand nombre de mesures de position)
- retours de l'utilisateur final/décideur très lents (mesure de position très
  rare)
- dialogue avec une API/base de donnée/système distant/... très lent (chaque
  mesure de position demande de très longs traitements)
- peu de confiance dans les résultats (nécessité de refaire plusieurs fois les
  mesures ou de les retraiter)


Un exemple concret
==================

Avec mon collègue David_ nous nous sommes chargés de la résolution d'un ticket
pour le projet AMO_.

.. _David: https://larlet.fr/david/
.. _AMO: https://addons.mozilla.org

Afin de pouvoir présenter des graphiques d'utilisation/téléchargement des
extensions à leur auteur (comme pour Firebug_), toutes les requêtes de
téléchargement et de demande de mise à jour sont enregistrées et stockées dans
une base de donnée « big data » (pour les curieux : c'est stocké dans Hadoop_
et récupéré par le biais de Hive_). On parle de plus d'un milliard de requête
par jour, toutes requêtes confondues.

.. _Firebug:
    https://addons.mozilla.org/en-US/firefox/addon/firebug/statistics/?last=30
.. _Hadoop: http://hadoop.apache.org/
.. _Hive: https://hive.apache.org/

Ce qui nous a d'abord paru simple et rapide à implémenter, s'est transformé en
deux semaines de sprint (et n'est pas encore terminé).

Nous avons subit et fait partie des différentes formes de latences listées
ci-dessus :

- besoin mal exprimé ou mal compris : la répartition des tâches entre nous et
  notre interlocuteur a changé plusieurs fois. Par ailleurs nous n'avions
  aucune connaissance du système avant de nous y attaquer.
- périmètre fonctionnel qui change : malheureusement, arrivé au bout de la
  première semaine de sprint, nous avons appris qu'il nous fallait refaire la
  moitié de notre travail différemment suite à des contraintes non prévues.
- grand nombre d'aller-retours avec l'utilisateur final/décideur : à l'heure de
  l'écriture de ce billet, nous en sommes à 54 commentaires sur le ticket.
- retours de l'utilisateur final/décideur très lent : nous travaillons en
  France, et notre interlocuteur sur la côte ouest des USA (-9h). Il est
  fréquent d'avoir besoin d'attendre le lendemain pour avoir une réponse, dans
  un sens ou dans l'autre.
- dialogue avec un système distant très lent : de par le nombre de données à
  traiter, chaque requête à Hive (au nombre de 6) prend en moyenne 15 minutes,
  et la taille des données à télécharger varie entre 500Mo et 1.6Go.
- peu de confiance dans les résultats : nous essayions de mettre au point les
  requêtes Hive à exécuter, et par le même temps, le post-traitement de ces
  requêtes, pour coller au plus proche aux statistiques et graphiques attendus.
  Jouer sur deux paramètres en même temps est déjà malaisé en temps normal,
  mais là il nous était de plus très laborieux de confronter nos résultats avec
  ceux de la production.


La solution
===========

Diminuer la latence dans la boucle de rétroaction, par tous les moyens
possibles.

De la même manière qu'il arrive régulièrement de lancer un interpréteur Python
(ou un *ipdb* ;) pour bidouiller et expérimenter avec un petit bout de code
et avoir des retours immédiats, il faut tout faire pour accélérer la boucle de
rétroaction.

- ça paraît évident, mais connaître précisément le besoin et le contexte avant
  de se lancer est primordial. Nous avons facilement perdu deux à trois jours à
  cause de ça, en début de sprint, avec notre envie d'avancer rapidement (et de
  passer à quelque chose de plus fun ;)
- périmètre fonctionnel qui change : difficile de le prévoir ou de l'éviter,
  mais je pense qu'en ayant une boucle de rétroaction plus courte, nous aurions
  eu des résultats plus rapidement, et aurions alors plus rapidement rencontré
  les contraintes qui ont fait changer le périmètre.
- le nombre d'aller-retours avec l'interlocuteur, et leur lenteur : quand nous
  avons pu mettre en place un appel vidéo journalier, beaucoup de choses se
  sont débloquées.
- dialogue avec le système distant très lent : nous aurions dû mock_ beaucoup
  plus tôt le retour des requêtes Hive. Nous aurions ensuite dû récupérer un
  jeu de donnée complet (plusieurs Go) le plus tôt possible pour faire des
  tests sur le post-traitement dans un premier temps, puis ensuite seulement
  essayer d'améliorer les requêtes Hive. Faire les deux en même temps est une
  erreur qui nous a coûté de nombreux appels à Hive (et donc de nombreuses
  attentes et rétro-pédalages).
- peu de confiance dans les résultats : encore une fois vu la taille des
  données à traiter, il nous était très difficile de confronter nos données à
  celles attendues (uniquement disponibles en production). Nous avons fini par
  mettre en production un post-traitement parallèle à l'actuel, et stocker les
  données dans d'autres tables, en attendant d'avoir la version finale et
  raffinée de l'algorithme et des requêtes.

.. _mock: http://www.voidspace.org.uk/python/mock/

Et à ma plus grande honte, ne pas avoir de tests unitaires a été un boulet
supplémentaire : lancer un post-traitement pour s'apercevoir 15 minutes plus
tard qu'on a oublié une virgule dans le code...
