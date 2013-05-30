Retour sur Sud Web 2013
#######################
:date: 2013-05-24 12:06
:category: misc


Le 17 et 18 mai, en Avignon, avait lieu la troisième édition de `Sud Web`_.
C'est une conférence que j'affectionne tout particulièrement, ayant eu la
chance de participer à son organisation à ses débuts.

.. _Sud Web: http://sudweb.fr/2013/

Le format est le suivant : une première journée de présentations, courtes (5mn)
et longues (20mn + 5mn de questions), et une deuxième journée
d'« élaboratoires ».


Les présentations
=================

Les présentations étaient pour la plupart sous la forme de retours
d'expérience. C'est à mon humble avis le format le plus intéressant : en effet,
les nouveautés techniques sont pléthores, et les technologies éprouvées sont
pour la plupart déjà connues.

Surtout dans une conférence généraliste de la sorte, présenter un point
technique très précis et pointu serait une perte de temps pour la majorité de
l'audience.


Le client, ce gentil méchant
----------------------------

Une petite piqûre de rappel : pour le client, c'est nous les méchants
développeurs. Alors oui, souvent le client doit être éduqué, accompagné,
conseillé, et la relation est souvent ardue, mais il ne faut pas oublier que
dans l'autre sens c'est vrai aussi : un client doit souvent éduquer et
conseiller un développeur, sur les côté produit/besoins.

Il faut en finir avec le dialogue de sourd entre client et développeur, qui
nuit aux deux parties. 


SASS et Compass ont embelli mon quotidien
-----------------------------------------

Retour d'expérience sur l'utilisation de SASS (et de Compass) par rapport à un
seul fichier CSS de plusieurs dizaines de milliers de lignes, impossible à
maintenir.

Medhi recommande d'ailleurs une architecture et un découpage des fichiers afin
de s'y retrouver plus rapidement, ainsi qu'une bonne documentation des règles
écrites : justifier un décalage de 10pixels, expliciter l'utilité d'un mixin,
etc...

Nous utilisons déjà SASS et Compass à Novapost, mais il reste un peu de travail
au niveau de l'organisation des fichiers et de leur découpage.


Getting touchy : an introduction to touch events
------------------------------------------------

Excellent exposé de Patrick sur les difficultés inhérentes à la gestions des
évènements *touch* sur les différents *devices* disponibles de nos jours.

Plusieurs soucis à prendre en compte :

* la gestion des évènements n'est pas la même sur tous les navigateurs et tous
  les *devices* (ordre, nombre, type...)
* les *hacks* peuvent être dangereux. Exemple : il est possible de désactiver
  le délai sur la détection d'un click (pour augmenter la réactivité et se
  rapprocher d'une application native), mais attention au fait que ça désactive
  par la même occasion la détection d'un double-click, le scroll, pinch &
  zoom...
* il y a des *devices* qui permettent d'utiliser une souris en parallèle du
  *touch*, comme certaines tablettes ou ordinateurs portables avec écran
  tactile. Dans ce cas, il faut réagir aux évènements *touch* mais aussi
  *mouse*


Le développement c'est difficile
--------------------------------

En prenant l'exemple de la gestion des dates et fuseaux horaire, Rémi nous
montre comment quelque chose qui a l'air simple en apparence, peut contenir des
pièges multiples dans lesquels même les plus grands (Apple, Microsoft...)
peuvent tomber.

A Novapost, lors du passage en Django1.4, nous avons déjà fait en sorte
d'utiliser les fonctionnalités de gestion des fuseaux horaire développées par
Aymeric Augustin, et pour l'instant, avec succès. Ce n'est malheureusement pas
une solution définitive, à chaque fois qu'on joue avec des dates ou des heures,
il faut garder en tête la problématique et bien penser à ce qu'on fait pour ne
pas retomber dans le piège.


Aubergine n'est pas une couleur
-------------------------------

Si le client vous parle d'une couleur, ne pas hésiter à lui faire confirmer
cette couleur par rapport à un référentiel couleur que vous auriez en commun.


L'odyssée de l'espace insécable
-------------------------------

Eh non, il n'y a pas qu'un seul et unique espace insécable. Oui, le plus connu
est le ``&nbsp;``, mais il en existe plusieurs autres qui devraient être
utilisés en lieu et place de celui-ci. La meilleure solution étant
d'automatiser tout ça.


Et si j'écrivais un livre ?
---------------------------

Retour de Corinne sur son aventure personnelle : c'est une expérience qui a
l'air attirante, mais qui est parsemée d'embûches, et il faut surtout faire
attention à la gestion de son temps, de sa motivation, et des retours faits par
les relecteurs.


Quête mystère
-------------

`La quête de sens`_, (non-)présentée et animée par David : échange avec le
public et entre le public sur diverses questions et thèmes

.. _La quête de sens: https://larlet.fr/david/blog/2013/quete-sens/

* argent : qui ferait le même métier si il était bien moins bien payé
  (exemple : payé au smic). Une grande majorité de l'assistance a dit oui,
  argumentant que beaucoup faisaient de l'open-source (bénévolement), et
  faisaient leur métier par passion
* utilité : la plupart sentent qu'ils ont beaucoup de pouvoir et d'utilité dans
  leur domaine, mais pas forcément dans leur mission ou emploi actuel
* adrénaline : peu de gens ont l'impression de faire ce métier pour
  l'adrénaline de la mise en production, du débug en prod...
* santé : constat alarmant, beaucoup ont des soucis de santé à cause de leur
  travail. En effet, le propre d'une passion est de prendre toute la place, et
  beaucoup se retrouvent en manque de sport, avec des soucis de dos, de stress,
  de burnout


Responsive news : l'actualité mobile à la BBC
---------------------------------------------

Kaelig nous a raconté son expérience à la BBC sur la mise en place de
« responsive web design » et leur méthode utilisée : au lieu de gérer les
spécificités d'une multitude de *devices*, ils ont décidé de placer un curseur,
et tous les téléphones qui supportent ce minimum de fonctionnalités ont la
version avancée (ajax, CSS3), les autres ayant une version statique basique.


La visualisation de données
---------------------------

... comme outil pour découvrir et partager des idées sur le Web. Exposé fort en
images et animations de Nicolas, vraiment bluffant.

On se rend compte que la bonne visualisation, selon le besoin, va avoir une
vraie valeur ajoutée : découvrir les éléments qui sortent de la moyenne en
regardant les directions et forces du vent, mettre en relation/opposition des
tweets de candidats à l'élection présidentielle, ainsi que leur impact sur les
états...

Certaines autres visualisations sont purement artistiques.


Les super-pouvoirs du nouveau venu
----------------------------------

Par votre humble serviteur (je n'ai pas pu assister aux deux présentations
courtes précédente, vu que je me préparais en coulisse).

En attendant la vidéo, vous pouvez `trouver le support ici`_.

.. _trouver le support ici: http://agopian.info/presentations/2013_05_sudweb/

Le but était de montrer qu'en mettant en place un système de mentorat, une
mise en relation entre un ancien et un nouveau, on a tout à y gagner.


Travailler sur ses deux pieds
-----------------------------

Considérations sur l'impact négatif sur la santé de travailler en position
assise toute la journée. De plus en plus de développeurs optent pour travailler
au moins une partie de la journée debout devant leur bureau (surélevé par
divers moyens).

Je teste cette méthode depuis plusieurs mois avec bonheur (et un soulagement au
niveau du dos). Pour ne pas trop stresser genoux et chevilles, j'alterne
régulièrement, passant parfois des jours d'affilée assis, et d'autre debout, ou
alternant plusieurs fois dans la même journée.


Monitoring : une culture plus que des outils
--------------------------------------------

Différentes expériences malheureuses ont conduit le journal `20minutes.fr`_ a
mettre en place un monitoring très fin des différentes parties de leur système.
Ça leur a permis de détecter très tôt (parfois avant même le retour de leurs
utilisateurs) de problèmes lors de la mise en production par exemple.

.. _20minutes.fr: http://20minutes.fr

À Novapost nous avons depuis peu trois gyrophares en plus du monitoring par
Sentry et New Relic : ils nous permettent de voir de manière ludique quelques
indicateurs de notre plateforme.


Comment l'impression 3D va modifier le Web et l'économie
--------------------------------------------------------

Marc, avocat très versé dans les nouvelles technologies, nous montre comment le
futur, c'est maintenant. La répliqueuse de Star Trek, qui nous faisait rêver en
étant enfant, devient une réalité avec les imprimantes 3D qui permettent
d'imprimer des organes humains, des bonbons, des objets de tout type.

Cela aura obligatoirement un fort impact sur les utilisations, l'économie et la
perception des droits d'auteur.


Les élaboratoires
=================

Les élaboratoires sont aussi souvent appelés « barcamps ». Le principe est
simple : plusieurs scéances dans la journée, proposées pour certaines avant le
jour J, d'autres le jour même, sur différents sujets, problématiques. Le but
unique est l'échange entre les participants, et est régi par la règle des deux
pieds : si tu n'as rien à apprendre ni rien à apporter, change de salle.

J'y ai appris comme faire des *mockups* d'applications mobiles, et pourquoi
Didier s'est noyé dans son code (enquête en fil rouge tout au long de la
journée sur la mise en place de méthodes agiles, l'importance de se soutenir
dans une équipe...).


Conclusion
==========

Encore une excellente édition : le plus important, non décrit ici, c'est la
possibilité d'échanges, de découvertes et de rencontres durant les pauses, lors
des soirées communautaires, tout au long de la journée d'élaboratoires.

Ces échanges et rencontres, ainsi que les présentations, m'ont permis de
repartir plein d'énergie, d'idées, d'envies d'expérimentations.

Ce genre de rencontre est à mon sens indispensable à tout développeur pour lui
éviter de s'enfermer dans sa cave, de se sur-spécialiser, de perdre le contact
avec ses pairs, et par là-même, de devenir obsolète.
