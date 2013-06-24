Retour sur Pytong 2013
######################
:date: 2013-06-24 10:22
:category: misc


Le 22 et 23 juin, à Toulon, s'est tenue la première édition de Pytong_,
organisée par `Laurent Paoletti`_ et `David Larlet`_ (merci à eux !).

.. _Pytong: http://pytong.org
.. _Laurent Paoletti: http://providenz.fr/
.. _David Larlet: https://larlet.fr/david/

Le format a reprit ce dont on a maintenant l'habitude pour les conférences
Django organisées par django-fr_, une première journée de conférences et
barcamps, et une deuxième journée de détente ensemble pour apprendre à mieux se
connaître.

.. _django-fr: http://django-fr.org


Les présentations
=================

Reporting web et pdf
--------------------

`Arthur Vuillard`_ nous a montré comment utiliser pygal_ pour faire de
jolis reporting web avec de jolis graphes SVG annotés, et weasyprint_ pour un
export en PDF propre, avec gestion des coupures de tableaux, centrage sur la
page, etc...

.. _Arthur vuillard: http://hashbang.fr
.. _pygal: http://pygal.org
.. _weasyprint: http://weasyprint.org


Tu peux WebTest
---------------

`Gaël Pasgrimaud`_, mainteneur de l'excellente librairie WebTest_ (créée par le
prolifique Ian Bicking), nous a expliqué comment l'utiliser pour tester nos
applications WSGI. Ça peut avantageusement remplacer le `Django Test Client`_,
étant donné ses fonctionnalités avancées, sa facilité d'utilisation, et le fait
que ça dialogue directement au niveau WSGI.

`Tu peux WebTest, les slides`_.

.. _Gaël Pasgrimaud: https://twitter.com/gawel_
.. _WebTest: https://webtest.readthedocs.org/en/latest/
.. _Ian Bicking: http://www.ianbicking.org/
.. _Django Test Client: https://docs.djangoproject.com/en/dev/topics/testing/overview/#module-django.test.client
.. _Tu peux WebTest, les slides: http://gawel.github.io/pytong2013_webtest/#/tu-peux-webtest


Des migrations sans interruption de service
-------------------------------------------

Thomas Chaumeny a listé plusieurs techniques et pratiques, ainsi que les
pièges à éviter pour faire des migrations de schéma de données (principalement
en utilisant South_), et ce sans interruption de service. En effet, selon la
migration, les changements dans la base de données peuvent bloquer une table
(verrou en écriture) pendant plusieurs minutes, voire heures. Il y a donc
certains pièges a éviter, et des méthodes à suivre.

`Des migrations sans interruption de service, les slides`_.

.. _South: http://south.aeracode.org/
.. _Des migrations sans interruption de service, les slides: http://polyconseil.github.io/presentations/no_downtime_migrations/


Débuter avec salt
-----------------

`Yann Malet`_ nous a fait une rapide présentation de Salt_, un gestionnaire de
configuration, un framework d'installation et d'exécution à distance. Pour ceux
qui connaissent Chef_ ou Puppet_, Salt est un remplaçant écrit en Python, très
performant, car basé sur 0MQ_.

Il a ensuite expliqué comment, à LincolnLoop_, ils ont utilisé Salt en tant que
framework d'exécution à distance pour leur nouveau projet de monitoring :
Salmon_.

.. _Yann Malet: https://twitter.com/gwadeloop
.. _Salt: http://saltstack.com
.. _Chef: http://www.opscode.com/chef/
.. _Puppet: http://puppetlabs.com/
.. _0MQ: http://zeromq.org
.. _LincolnLoop: http://lincolnloop.com
.. _Salmon: https://github.com/lincolnloop/salmon


Déprimé, au bord du burn-out, et pourtant il faut continuer à coder
-------------------------------------------------------------------

`Jean-Michel Armand`_ nous a fait part de son expérience de surmenage, de
comment il s'en est sorti, et comment il essaie de ne plus se mettre en danger
physiquement et psychologiquement. Un paquet de conseils avisés, à suivre avant
qu'il ne soit trop tard.

On dit souvent qu'il faut vivre ses propres expériences pour pouvoir en
apprendre, et j'ai moi-même vécu une expérience similaire. Les conseils donnés
dans cette présentation sont précieux, et peuvent se résumer à « vous valez
mieux que votre code/travail, vivez ».

`Déprimé, au bord du burn-out... les slides`_.

.. _Jean-Michel Armand: http://j-mad.com
.. _Déprimé, au bord du burn-out... les slides: https://speakerdeck.com/mrjmad/deprime-au-bord-du-burn-out-et-pourtant-il-faut-continuer-a-coder


Mezzanine, le CMS des développeurs pragmatiques
-----------------------------------------------

`Thibault Jouannic`_ nous a parlé de Mezzanine_, un CMS simple, performant et
facilement extensible, qui permet de répondre à des demandes simples sans avoir
à installer un Drupal ou Wordpress.

.. _Thibault Jouannic: http://miximum.fr
.. _Mezzanine: http://mezzanine.jupo.org/


Use 0MQ and Tornado for fun and profit
--------------------------------------

`Boris Feld`_ nous a donné des recettes pour utiliser 0MQ_ avec Tornado_ pour
faire le lien avec HTTP.

`Use 0MQ and Tornado for fun and profit, les slides`_.

.. _Boris Feld: http://feldboris.alwaysdata.net/blog/
.. _Tornado: http://www.tornadoweb.org/
.. _Use 0MQ and Tornado for fun and profit, les slides: https://speakerdeck.com/lothiraldan/use-omq-and-tornado-for-fun-and-profits


Écriture d'un livre sur Django
------------------------------

`Yohann Gabory`_ nous a parlé de son expérience d'écriture d'un livre sur
Django : `Django avancé`_. Il en a profité pour nous expliquer comment écrire
une bonne documentation utilisateur, pour lui donner envie d'utiliser notre
projet/librairie/application...

`Écriture d'un livre sur Django, les slides`_.

.. _Yohann Gabory: https://twitter.com/boblefrag
.. _Django avancé: http://www.eyrolles.com/Informatique/Livre/django-avance-9782212134155
.. _Écriture d'un livre sur Django, les slides: http://fr.slideshare.net/YohannGabory/pytong-2013


Python dans le navigateur, et pourquoi pas
------------------------------------------

`Jean-Michel Armand`_ nous a fait une démonstration de Brython_, vu que toute
sa présentation était faite avec. Brython a pour ambition de remplacer
JavaScript dans le navigateur par le langage Python.

.. _Brython: http://brython.info


Python(Script) par Python pour le navigateur
--------------------------------------------

`Amirouche Boubekki`_ nous a parlé de son projet PythonScript_, une autre
alternative à Brython pour avoir du Python dans le navigateur.

.. _Amirouche Boubekki: https://plus.google.com/116302792447642827163/posts
.. _PythonScript: https://pythonscript.readthedocs.org/


JavaScript pour les développeurs Python
---------------------------------------

`Nicolas Perriault`_ a pris à revers les deux précédentes présentations
courtes : il explique qu'il est inutile et futile de vouloir remplacer le
langage qui a été prévu exprès pour manipuler le DOM et être asynchrone (à base
de callbacks), exprès pour être exécuté dans les navigateurs.

Le pragmatisme du développeur Python voudrait justement qu'il utilise les bons
outils pour les bonnes utilisations, et donc JavaScript pour du code dans le
navigateur.

.. _Nicolas Perriault: https://twitter.com/n1k0


Développer une app Django
-------------------------

`Samuel Goldszmidt`_ s'est servi de l'exemple de son application
Django-Select2Light_ pour montrer comment créer une application Django, en
utilisant FloppyForms_ et TastyPie_.

`Développer une app Django, les slides`_.

.. _Samuel Goldszmidt: https://twitter.com/ouhouhsami
.. _Django-Select2Light: https://github.com/ouhouhsami/django-select2light
.. _Floppyforms: http://django-floppyforms.readthedocs.org/en/latest/
.. _TastyPie: http://tastypieapi.org/
.. _Développer une app Django, les slides: https://raw.github.com/ouhouhsami/pytong2013-LT-django-app-development-/master/slides.txt


Utiliser un système de packaging privé
--------------------------------------

Brice Gelineau nous a expliqué comment il utilisait un système de packaging
privé pour son déploiement. C'est encore une autre alternative à l'utilisation
de Buildout_ ou encore le `mirroir PyPI privé`_ dont j'ai eu l'occasion de
parler lors d'une précédente conférence.

`Utiliser un système de packaging privé, les slides`_.

.. _Buildout: http://buildout.org
.. _mirroir PyPI privé: ../le-miroir-pypi-du-pauvre.html
.. _Utiliser un système de packaging privé, les slides: http://polyconseil.github.io/presentations/private_packaging/


À quoi ressemblerait mon python ?
---------------------------------

`Nicolas Dubois`_ s'est demandé comment améliorer encore la lisibilité de nos
programmes Python. Il s'avère qu'avec quelques judicieuses modification, et
l'utilisation de caractères Unicode par exemple, nous pourrions avoir du code
source encore plus concis et expressif.

Il y a peu de chances que nous ayons un interpréteur Python comprenant cette
syntaxe un jour, mais je trouve très intéressant de se poser ce genre de
questions, et nous avons commencé a écrire « BMC » (Beautify My Code) avec
Nicolas, petite librairie (service ?) qui permet d'opérer des
changements/remplacements sur un fichier source et d'afficher le résultat. À
suivre donc.

`À quoi ressemblerait mon python, les slides`_.

.. _Nicolas Dubois: https://twitter.com/duboisnicolas
.. _À quoi ressemblerait mon python, les slides: http://git.nicolasdubois.com/talks/2013-pytong/


Daybed, une couche de validation pour CouchDB
---------------------------------------------

`Antoine Cezar`_ nous a présenté le projet Daybed_ dont il est un des
contributeurs. Cette surcouche à CouchDB, qui ajoute la validation de données,
permet d'avoir un remplaçant à GoogleForms_.

`Daybed, une couche de validation pour CouchDB, les slides`_.

.. _Antoine Cezar: http://blog.antoine.cezar.fr/
.. _Daybed: http://daybed.readthedocs.org/en/latest/
.. _GoogleForms: http://docs.google.com/forms
.. _Daybed, une couche de validation pour CouchDB, les slides: https://github.com/AntoineCezar/pytong-2013-daybed-slides


Les barcamps
============

Les Web Components
------------------

Il y a eu un premier barcamp proposé par `David Larlet`_ qui a fait l'unanimité
(oui, c'est bizarre d'avoir un seul et unique barcamp, ça s'oppose un peu à la
loi des deux pieds) : une présentation des Web Components.

Les Web Components ont à l'heure actuelle deux implémentations : celle de
Mozilla avec xtags_, et celle de Google avec polymer_. Ce sont des composants
qui peuvent être entièrement packagés et distribuables : html, css et
JavaScript en un seul morceau.

Ça me laisse une sorte d'impression de déjà vu, comment si on revenait aux
années sombres des « clients lourds » avec GUI, composants et widgets, etc...
je vois néanmoins l'intérêt que ces Web Components apportent alors qu'on
déporte de plus en plus de logique et de calcul sur le client, et qu'on cherche
à avoir des applications web de plus en plus proches, justement, des
applications natives.

.. _xtags: https://github.com/mozilla/xtags-org/tree/master/public
.. _polymer: http://www.polymer-project.org/


Comprendre "this" en JavaScript
-------------------------------

Suite à sa présentation courte sur « JavaScript pour les développeurs Python »,
`Nicolas Perriault`_ a indiqué les différentes utilisations et manières de
spécifier *this* en JavaScript, ainsi que les IIFE_ et *use strict*.

J'avais déjà eu la chance de me pencher sur l'utilisation de *this* grâce à un
lien que Nicolas m'avait fourni : `Learning advanced JavaScript`_.

.. _IIFE: http://benalman.com/news/2010/11/immediately-invoked-function-expression/
.. _Learning advanced JavaScript: http://ejohn.org/apps/learn/


Maitriser git
-------------

Proposé par `Thibault Jouannic`_, je n'ai pu y participer ayant assisté au
barcamp ci-dessus, mais j'en ai eu de bons retours.


La journée détente
==================

Au programme :

- plage + baignade : pour les plus courageux, l'eau n'étant pas très chaude, et
  le vent était assez violent et frais
- slackline : première fois pour moi, génial ! J'ai hâte de pouvoir en refaire
- repas : bon, convivial, à l'ombre des mûriers platane, vue sur la mer, que
  demander de plus
- jeux de société : Dixit, Pandémie
- pétanque
- `marshmallow challenge`_ animé par `Stéphane Langlois`_.Sympa de voir la
  rétrospective, sur comment les enfants ont parfois de meilleurs résultats que
  les jeunes ingénieurs ou commerciaux !

.. _marshmallow challenge: http://marshmallowchallenge.com/Instructions.html
.. _Stéphane Langlois: https://twitter.com/pointbar


Conclusion
==========

C'est toujours un vrai plaisir de pouvoir rencontrer ses pairs, apprendre
d'eux, échanger, faire connaissance, échanger des astuces et techniques. Je
pense que c'est un investissement indispensable à tout développeur passionné et
curieux qui souhaite évoluer et rester au courant des avancées dans son
domaine.

Vous pouvez par ailleurs consulter le `compte rendu de Rémy`_.

.. _compte rendu de Rémy: http://tech.novapost.fr/pytong-2013-a-toulon-le-resume.html

Enfin, en petit bonus, je vous met le lien vers la présentation courte que
j'avais préparée « au cas où », mais que je n'ai pas eu l'occasion de montrer :
`Sécuriser ses données`_.

.. _Sécuriser ses données: http://mathieu.agopian.info/presentations/2013_06_pytong/
