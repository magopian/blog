PyCon.fr 2010 : retour sur une conférence organisée par l'AFPY
##############################################################
:date: 2010-08-30 08:53
:category: django
:tags: conference

`Cette édition de PyCon.fr`_ était la deuxième à laquelle j'ai assisté.
Elle s'est déroulée, comme l'année dernière, à la CyberBase de la Cité
des Sciences à la Villette, Paris.

Et comme l'année dernière, j'ai apporté ma maigre contribution à
l'organisation sur place, aux côté des super-motivés de l'`Association
Francophone PYthon`_ (liste non exhaustive : Christophe Combelles,
Michael Scherrer, Gaël Pasgrimaud, Jean-Philippe Camguilhem, Olivier
Grisel).

Le cadre
~~~~~~~~

Nous avons été encore une fois super bien accueillis par la CyberBase.
A disposition, un amphitéatre et une "base technique" (salle équipée de
nombreux ordinateurs, idéale pour les mises en applications et les
travaux pratiques). Les deux salles ont tout l'équipement nécessaire
pour la rétro-projection des présentations, et avaient cette année
encore la couverture vidéo de `Ubicast`_.

Les sponsors
~~~~~~~~~~~~

Vous trouverez la `liste des généreux sponsors`_ sur le site de
`PyCon.fr 2010`_. C'est en très grande partie grâce à eux qu'une telle
conférence peut être organisée, en restant gratuite, j'en profite donc
pour les remercier à nouveau (et les encourager à recommencer l'année
prochaine bien évidemment ;).

Nous avons entre autres eu des présentations de plusieurs produits
libres et open-source des sponsors `Logilab`_ (avec leur solution Cubic
Web qui fait tourner le site de `pycon.fr`_) et `Itaapy`_.

Les présentations
~~~~~~~~~~~~~~~~~

Vous trouverez là aussi la liste sur le site de pycon.fr, et je vais
lister ici les présentations auxquelles j'ai pu assister et qui m'ont
marqué (les autres je les verrais en vidéo, grâce à `Ubicast`_, dès
qu'elles seront en ligne) :

-  plusieurs lightning talks, en particulier sur Pyaler, le GSoC sur
   distutils 2 (vivement que ça sorte!), pysandbox, restkit
-  Optimisation d'applications Django de Bruno Renié (mon co-champion
   "planet" pour `django-fr`_ ;) : plein d'astuces pour limiter le
   nombre de requêtes, utiliser le cache de manière intelligente ...
-  MongoKit de Nicolas Clairon : comment utiliser une base NoSQL MongoDB
   facilement et efficacement avec MongoKit
-  Analyse statistique et classification automatique de texte de Olivier
   Grisel : ça m'a replongé dans mon mémoire de DEA sur l'apprentissage
   automatique ;)
-  l'incontournabl)e Gunicorn de Benoit Chesneau : à mon avis, l'un des
   plus grands pas en avant pour rendre python (et `Django`_) très
   facilement déployable
-  Construire un CMS sur mesure avec Django de Yann Malet : il faut
   arriver à vendre non pas du forfait (trop risqué pour le développeur,
   trop cher pour le client, et risque d'effet tunnel), mais des cycles
   de développement (par exemple de deux semaines, avec review +
   paiement à chaque cycle, puis décision sur le cycle suivant). Voilà
   quelque chose qui me plait, mais qui est très difficile à vendre à
   des clients qui veulent surtout pouvoir chiffrer de manière très
   précise leur budget
-  Programmation en Flux de Jonathan Schemoul : présentation de `PyF`_
   qui permet de traiter de très nombreuses données en limitant la
   mémoire utilisée (grâce aux "flux"). Très intéressant, et un outil
   graphique en ligne qui m'a l'air très simple et pratique
   d'utilisation

Les rencontres
~~~~~~~~~~~~~~

J'ai pu revoir nombre de personnes déjà rencontrées à l'édition de
l'année précédent de PyCon.fr, ainsi qu'à `Djangocong`_, personnes que
je connaissais déjà auparavant par internet (irc, twitter, mailing lists
de l'afpy et de django-fr ...). Revoir "en vrai" des personnes qu'on
côtoie très souvent de manière électronique est pour moi toujours une
joie et un enrichissement, car l'échange est bien plus facile, et on
tisse des liens bien plus étroits autour d'une bière que par internet!

Et comme je l'ai `déjà twitté`_, j'ai par ailleurs été ravi de faire de
nouvelles connaissances, que j'espère pouvoir revoir bientôt (un an
entre chaque pycon.fr, ça fait long!). Il paraît qu'il devrait y avoir
d'ici peu un autre `afpyro national`_ organisé, il faudra essayer de
rassembler les troupes sur Sophia/Nice à cette occasion! Peut-être une
occasion de tester le pastis magique de Jean-Philippe (il m'a promis
qu'il ferait un article là-dessus, que je lierai ici ;)

Les bonus
~~~~~~~~~

Comme si cela ne suffisait pas, il y a eu quelques bonus très
sympathiques :

-  un écran géant et tactile dans la CyberBase qui affichait en boucle
   `isparade.jp sur le mot clé #pyconfr`_
-  j'ai découvert `aspirator`_ de Bruno Renié, un news reader fait en
   django, et qui à l'air vraiment génial... ce gars est vraiment doué,
   ça en est limite énervant ;). Il travaille aussi sur wombat, un
   projet de client mail
-  j'ai revu une bonne partie de mon ex équipe de badminton qui prenait
   le même avion que moi! (ils étaient aux championnats du monde qui
   avait lieu ce même week-end sur Paris)
-  Alexis Métaireau (`@ametaireau`_) nous a parlé de son travail pour le
   GSoC avec Tarek Ziadé sur distutils 2 : vivement que ce soit dans la
   stdlib!
-  Rémi Ubscher (`@natim`_) est Eclaireur lui aussi! Salut Fennec ;)
-  Benoit Calvez (`@\_dzen`_) m'a parlé de `fabulator`_ et de
   `vineolia`_ : énorme potentiel (et il a d'autres projets dans les
   cartons ;)

Conclusion
~~~~~~~~~~

Vivement la prochaine édition (peut-être sur Pau? ping Jean-Philippe ;)
et d'ici là, peut-être une nouvelle édition d'une rencontre Django en
france!

Encore un énorme merci aux organisateurs, sponsors, présentateurs, et
aux participants, qui font de cet évènement un moment agréable et
enrichissant!

.. _Cette édition de PyCon.fr: http://www.pycon.fr/conference/edition2010
.. _Association Francophone PYthon: http://afpy.org
.. _Ubicast: http://ubicast.eu
.. _liste des généreux sponsors: http://www.pycon.fr/view?rql=Any+X,XD,RT+WHERE+C+eid+1450,+R+sponsoring_conf+C,+X+is_sponsor+R,+R+title+RT,+X+description+XD
.. _PyCon.fr 2010: http://www.pycon.fr/conference/edition2010
.. _Logilab: http://www.logilab.fr
.. _pycon.fr: http://pycon.fr
.. _Itaapy: http://itaapy.com
.. _django-fr: http://django-fr.org
.. _Django: http://www.djangoproject.com/
.. _PyF: http://www.pyfproject.org/
.. _Djangocong: http://rencontres.django-fr.org/
.. _déjà twitté: http://twitter.com/magopian
.. _afpyro national: http://www.afpy.org/Members/jpcw2002/national_afpyro_juillet_2010
.. _isparade.jp sur le mot clé #pyconfr: http://isparade.jp/334515
.. _aspirator: http://bitbucket.org/bruno/aspirator/wiki/Home
.. _@ametaireau: http://twitter.com/ametaireau
.. _@natim: http://twitter.com/natim
.. _@\_dzen: http://twitter.com/_dzen
.. _fabulator: http://bitbucket.org/dzen/fabulator/overview
.. _vineolia: http://vineolia.fr/
