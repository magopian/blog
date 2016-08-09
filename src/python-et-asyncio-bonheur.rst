Python et asyncio : la recette du bonheur ?
###########################################
:date: 2016-08-09 10:57
:category: python


`asyncio` est une librairie inclue dans la `stdlib` des dernières versions de
python3, et qui permet de faire de la programmation asynchrone.

Oui, ok, mais ça veut dire quoi au juste ?


Asynchrone, concurrent, coroutine, parallèle
============================================

Il y a un intrus dans ce titre. Ces termes sont utilisés pour décrire des
styles de programmation, mais sont parfois mal compris, ou prêtent à
confusion :

- asynchrone == concurrent == un seul process, dans lequel plusieurs morceaux
  de code, les `coroutines`, s'exécutent l'une après l'autre, dans le désordre,
  de manière non bloquante (on va y revenir)
- parallèle == multiprocessing == plusieurs process se partagent un ou
  plusieurs morceaux de code, morceaux qui s'exécutent **en même temps**, sur
  plusieurs processeurs/cœurs/machines


L'approche asynchrone/concurrente/non bloquante est légere tant à
l'implémentation qu'à l'execution - les `coroutines` sont très peu gourmandes
en mémoire et très rapides à lancer. Elles s'exécutent au sein du même process,
ont toutes accès à la même zone mémoire et il n'est donc pas nécessaire
d'échanger des messages entre elles pour partager des informations.
Cependant, elles n'accélèrent pas le programme car il n'y a toujours qu'un seul
process. Le programme ne sera donc plus rapide que dans certains cas
particuliers. Dans d'autres, il pourra même être plus lent à cause du surcoût
de gestion impliqué par l'utilisation de `coroutines`.

Dans une approche parallèle, le programme s'exécute sur plusieurs process, ce
qui l'accélère mécaniquement jusqu'à potentiellement diviser sa durée
d'execution par le nombre de coeurs mobilisés. Selon les langages et les
libraries utilisées, il est par ailleurs possible de lancer un programme sur
plusieurs machines. C'est une approche beaucoup plus lourde tant à
l'implémentation qu'à l'éxécution, car il faut lancer, synchroniser et arréter
chaque processus, qui en sus demande davantage de mémoire et l'utilisation d'un
système de message pour échanger avec ses voisins.


Oui, d'accord, mais comment ça marche ?
=======================================

Suivant les langages, il y a différentes façons de concevoir l'exécution
asynchrone et/ou de faire des appels non bloquants:

- en javascript : un appel asynchrone rend la main directement et passe à la ligne
  suivante. Son résultat est ensuite récupéré par le biais d'un `callback`.
- en clojure ou en go : des `canaux` sont utilisés pour envoyer et recevoir des
  messages. Ils sont assimilables à des tapis roulants entre deux morceaux de
  programmes, l'un qui pose des messages dessus quand bon lui semble, l'autre
  que les récupère également quand il le peut. Les deux bouts de code sont donc
  désynchronisés et ne se bloquent pas l'un l'autre.
- en python : un appel asynchrone passe par l'utilisation de générateurs,
  appelées `coroutines` dans le cas de `asyncio`. Dans ce cas, on gère
  explicitement la boucle d'exécution.

Dans le cas de python/`asyncio`, c'est grâce aux mots-clés ``await`` (ou
``yield from``) qu'un bout de code signale à la boucle d'exécution qu'il a
temporairement terminé sa tâche. Cette dernière passe donc la main à d'autres
bouts de code qui ont quelque chose à faire, au lieu d'attendre
séquentiellement (de manière synchrone) que chaque bout de code se termine.


Asynchrone == plus rapide, ou pas...
====================================

Mais alors, si le code s'exécute toujours sur un seul et même process et que la
gestion des `coroutines` implique un surcoût de temps de calcul, est-ce que mon
programme ne va être plus lent ?!

Petite expérience :

En synchrone/bloquant

::

    import asyncio

    def foo():
        pass

    for i in range(10000):
        foo()

::

    real    0m0.087s
    user    0m0.071s
    sys     0m0.013s



En asynchrone/non bloquant

::

    import asyncio

    async def foo():
        pass

    loop = asyncio.get_event_loop()
    for i in range(10000):
        loop.run_until_complete(foo())

::

    real    0m0.452s
    user    0m0.429s
    sys     0m0.019s


Un rapide calcul indique que la gestion des 10000 `coroutines` implique un
surcoût d'environ 360ms (l'import du module `asyncio`, qui se fait une seule
fois au chargement du programme, a été fait dans les deux cas afin de ne pas
fausser les mesures).

Le but de cet exemple aberrant n'est pas de prouver que les `coroutines` sont
lentes (elles ne le sont pas), mais que la programmation asynchrone en
elle-même ne fait pas aller n'importe quel programme plus vite (mais ça, vous
vous en doutiez).


Asyncio plus rapide pour IO-bound
=================================

Mais alors, `asyncio` ne sert à rien ?

Laissez-moi vous conter l'histoire de Bob, qui veut télécharger toutes les
images de chat de son site préféré.  Voici un petit morceau de son (pseudo-)
code :

::

    for url in urls:
        img = get_image_from_website(url)
        thumbnails = compute_thumbnails(img)
        ...

Le programme va tour à tour télécharger les images sur le site, puis en faire
des miniatures. Il y a donc deux cas différents :

- le téléchargement de l'image depuis le site, qu'on dit "IO-bound", car limité
  (lié) par l'IO (l'input-output, entrée sortie, tout échange entre le
  programme et l'extérieur). Pendant ce téléchargement, le programme va passer
  la majeure partie du temps à attendre que la requête soit reçue par le
  serveur distant, puis traitée, puis que les données soient envoyées, puis
  reçues. Pendant tout ce temps, le programme est bloqué, et ne fait rien
  d'autre. C'est un appel bloquant.
- le calcul de la miniature, qu'on dit "CPU-bound", c'est-à-dire limité (lié)
  par le CPU, par la puissance de calcul de l'ordinateur, du process qui fait
  tourner le programme. Aucune attente ici. Plus il y a de puissance de calcul
  (plus le processeur est rapide, plus il y a de CPU disponible), plus le
  programme ira vite.

L'idéal serait de pouvoir calculer la miniature d'une image pendant le temps
d'attente du téléchargement d'une autre image ! C'est une technique connue
depuis bien longtemps dans l'industrie, le "travail en temps masqué" : pendant
qu'une machine travaille, l'employé peut faire autre chose, comme remplir le
chargeur de la machine, décharger les produits finis, lancer une autre machine,
etc...

C'est la grande force de `asyncio` : pouvoir faire des appels non bloquants,
c'est à dire profiter d'un temps d'attente pour pouvoir faire autre chose.

Reprenons notre exemple :

En synchrone/bloquant

::

    import requests
    from lxml import html
    from PIL import Image

    URL_TPL = "http://bonjourlechat.tumblr.com/page/{}"
    THUMBNAIL_SIZES = ((100, 100), (200, 200), (300, 300), (400, 400), (500, 500))

    def get_image_from_website(url):
        page = requests.get(url)
        # Get the html content as a tree.
        tree = html.fromstring(page.content)
        # Use xpath to get the image url.
        img_url = tree.xpath('//figure//img/@src')[0]
        data = requests.get(img_url, stream=True)
        data.raw.decode_content = True
        img = Image.open(data.raw)
        return img

    def compute_thumbnails(img):
        thumbnails = []
        for size in THUMBNAIL_SIZES:
            thumbnails.append(img.thumbnail(size))
        return thumbnails

    def get_all_thumbnails():
        for i in range(1, 11):
            img = get_image_from_website(URL_TPL.format(i))
            thumbnails = compute_thumbnails(img)

    get_all_thumbnails()

::

    real    0m9.722s
    user    0m0.466s
    sys     0m0.089s

Soit environ 10 secondes, une seconde par image.


En asynchrone/non bloquant

::

    import aiohttp
    import asyncio
    from io import BytesIO
    from lxml import html
    from PIL import Image

    URL_TPL = "http://bonjourlechat.tumblr.com/page/{}"
    THUMBNAIL_SIZES = ((100, 100), (200, 200), (300, 300), (400, 400), (500, 500))

    async def get_image_from_website(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as page:
                # Get the html content as a tree.
                tree = html.fromstring(await page.text())

            # Use xpath to get the image url.
            img_url = tree.xpath('//figure//img/@src')[0]

            # Store the raw image data in a file-like object that Pillow can use.
            memfile = BytesIO()
            async with session.get(img_url) as data:
                memfile.write(await data.read())

        img = Image.open(memfile)
        return img

    async def compute_thumbnails(img):
        thumbnails = []
        for size in THUMBNAIL_SIZES:
            thumbnails.append(await loop.run_in_executor(None, img.thumbnail, size))
        return thumbnails

    async def get_thumbnail(url):
        img = await get_image_from_website(url)
        thumbnails = await compute_thumbnails(img)


    tasks = [get_thumbnail(URL_TPL.format(i)) for i in range(1, 11)]
    loop = asyncio.get_event_loop()
    thumbnails = loop.run_until_complete(asyncio.gather(*tasks))

::

    real    0m4.139s
    user    0m0.795s
    sys     0m0.094s

Soit environ 4 secondes, 0.5 seconde par image.

Plusieurs remarques :

- dans le cas du code asynchrone, il faut faire bien attention d'utiliser
  uniquement des appels non bloquants. On utilise donc `aiohttp` pour récupérer
  la page et l'image, puis faire les miniatures (en utilisant
  ``loop.run_in_executor``).
- plus le code dans ``compute_thumbnails`` sera gourmand en CPU, et sera donc
  long a exécuter, plus on gagnera en performance sur la version asynchrone par
  rapport à la version synchrone, le temps de CPU étant "masqué" par le temps
  du téléchargement des pages et des images.
- le code asynchrone est plus long, plus complexe, et nécessite de penser le
  programme différemment.
- le debugging de code asynchrone est également plus complexe (voir `ici <https://docs.python.org/3/library/asyncio-dev.html#debug-mode-of-asyncio>`_ et `là <https://pymotw.com/3/asyncio/debugging.html>`_)


Attention aux pièges
====================

::

    import asyncio
    import time

    async def foo():
        for i in range(10):
            await loop.run_in_executor(None, time.sleep, 1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(foo())

::

    real    0m10.137s
    user    0m0.079s
    sys     0m0.017s

Comment ça, 10 secondes ? Pourtant, les 10 appels à ``time.sleep(1)`` semblent
asynchrones, non bloquants, concurrents, dans des `coroutines` qui vont bien ?!

Il y a un piège: dans le code ci-dessus les 10 `coroutines` sont exécutées
**les unes après les autres**. Il pourrait être réécrit de la façon suivante,
qui met bien en valeur le problème :

::

    import asyncio
    import time

    async def foo():
        await loop.run_in_executor(None, time.sleep, 1)

    loop = asyncio.get_event_loop()
    for i in range(10):
        loop.run_until_complete(foo())

Lorsqu'une `coroutine` se lance, on attend qu'elle se termine avant d'en lancer
une autre. La façon correcte d'écrire ce code est de lancer toutes les
`coroutines` en même temps avec ``asyncio.wait()`` ou ``asyncio.gather()``
comme ci-dessous :

::

    import asyncio
    import time

    async def foo():
        await loop.run_in_executor(None, time.sleep, 1)

    loop = asyncio.get_event_loop()
    tasks = [foo() for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))


Asyncio est inutile pour CPU-bound
==================================

La programmation asynchrone par `coroutines` n'est utile que pour les cas
IO-bound : lecture/écriture sur le système de fichier, sur un socket...

Il faut imaginer un process comme étant Jean-Michel CPU, employé de Prog-corp,
auquel le programme demande d'exécuter une liste de tâches. Si Jean-Michel est
déjà surchargé de travail, réarranger ses tâches, les mettre dans le désordre,
bloquantes ou non bloquantes, ne changera rien du tout.

Par contre, si Jean-Michel CPU est en train de se tourner les pouces pendant que
Bernard IO est en train de trimmer à transporter des paquets de gauche et de
droite, alors les choses peuvent être optimisées :

En synchrone/bloquant :

- Prog-corp : Bernard IO, j'ai besoin d'un paquet steuplé
- Bernard IO : ok, **bouge pas**, j'y vais
- ... <un certain temps s'écoule> ...
- Bernard IO : pouf pouf, fatiguant tout ça, vla un paquet
- Prog-corp : Jean-Michel CPU, tu m'ouvres ça steuplé, tu tries, tu ranges...
- Jean-Michel CPU : ok, **bouge pas**, je m'y met
- ... <un certain temps s'écoule> ...
- Jean-Michel CPU : la vache, y'avait du bouzin, vla j'ai fini
- Prog-corp : Bernard IO, un autre paquet steuplé
- Bernard IO : ok, **bouge pas**, j'y vais
- ... <un certain temps s'écoule> ...
- ...

En asynchrone/non-bloquant :

- Prog-corp : Bernard IO, j'ai besoin d'un paquet steuplé
- Bernard IO : ok, je te préviens quand je l'ai
- ... <un certain temps s'écoule> ...
- Bernard IO : pouf pouf, fatiguant tout ça, vla un paquet
- Prog-corp : Bernard IO, ok merci, file m'en chercher un autre, kthxbye
- Prog-corp : Jean-Michel CPU, tu m'ouvres ça steuplé, tu tries, tu ranges...
- Jean-Michel CPU : ok, je te préviens quand je me tourne les pouces
- Bernard IO : pouf pouf, fatiguant tout ça, vla un paquet
- Prog-corp : Bernard IO, ok merci, file m'en chercher un autre, tu seras bien
  urbain
- Jean-Michel CPU : la vache, y'avait du bouzin, mais c'est bon j'ai fini
- Prog-corp : Jean-Michel CPU, ah bah pas trop tôt, voilà un autre paquet
- ...

Voilà un autre cas qui a l'air d'être IO-bound, sans que ce soit pourtant le
cas :

- Prog-corp : Bernard IO, j'ai besoin du résultat de cette requête SQL
- Bernard IO : ok, je te préviens quand je l'ai
- Bernard IO : hop hop, le voilà
- Prog-corp : euh, pardon ? Déjà !
- Bernard IO : ouais parce que en fait, on dirait pas, mais une database c'est
  genre ultra méga hyper rapide, tavu
- Prog-corp : Bernard IO, ok merci, file m'en chercher un autre, kthxbye
- Bernard IO : hop hop, le voilà
- Prog-corp : euh, oui, ok, mais euh, deux sec là, je suis occupé
- Bernard IO : hop hop, en voilà un autre
- Bernard IO : hop hop, tiens, encore un
- Prog-corp : Bernard IO, ouais non mais c'est bon, merci, attends un peu
  steuplé, chuis débordé, et puis Jean-Michel CPU arrive pas à suivre de toute
  manière
- ...

Les bases de données sont en général bien plus rapides que n'importe quel
programme écrit en python. Si, en théorie, une requête à la base de donnée est
une lecture/écriture (Input-Output), dans la pratique sa réponse arrive
tellement rapidement qu'il n'y a souvent rien à gagner à l'implémenter en
asynchrone. Si la base de données est distante, et que le délai (le round-trip)
est long, il est possible d'espérer gagner un peu. En général ce n'est pas le
cas (et si ça l'est, vous avez d'autres soucis à régler, en particulier au
niveau de la base de donnée elle-même). Pire, on perd le temps de la gestion
des `coroutines`.

La programmation asynchrone est vraiment efficace et utile dans quelques cas
notables, comme par exemple les lecture/écriture sur un système de fichier ou sur
un socket vers un serveur distant.

Gérer des requêtes entrantes sur un serveur web de manière asynchrones grâce à
`aiohttp`, ou des requêtes à postgresql avec `aiopg` (`probablement inutile
<http://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/>`_,
comme vu plus haut ?), ou avec le tout nouveau `asyncpg`, et plus important que
tout, télécharger des photos de chat. Voilà les exemples les plus courants
croisés dans les tutoriels.

Certains problèmes sont très pénibles à écrire de manière
synchrone/séquentielle, alors qu'ils s'expriment de manière tout à fait logique
de manière asynchrone. Par exemple un moteur de jeu : une `coroutine` qui gère
l'affichage en continu, et d'autres `coroutines` pour récupérer/traiter les
entrées du joueur.

Merci à `Aurélien G. <https://twitter.com/Alatitude77>`_ pour la `relecture et réécriture de l'article <https://github.com/magopian/blog/pull/1>` afin de le rendre plus agréable à lire !

