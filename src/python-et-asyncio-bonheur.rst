Python et asyncio : la recette du bonheur ?
===========================================

Asyncio est une librairie (qui fait partie de la stdlib dans les dernières
versions de python3) qui permet de faire de la programmation asynchrone.

Oui, ok, mais ça veut dire quoi au juste ?


Asynchrone, concurrent, coroutine, parallèle
---------------------------------------------

Il y a un intrus dans ce titre. Ce sont plusieurs termes qui sont utilisés pour
parler de styles de programmation, mais qui sont parfois mal compris, ou qui
prêtent à confusion :

- asynchrone == concurrent == un seul process, plusieurs morceaux de code
  (coroutines) qui s'exécutent l'un après l'autre, dans le désordre, de manière
  non bloquante (on va y revenir), sur le même process
- parallèle == multiprocessing == plusieurs process, plusieurs morceaux de code
  (ou le même), qui s'exécutent **en même temps**, sur plusieurs
  processeurs/cœurs/machines


Les avantages de l'asynchrone/concurrent/non bloquant : très léger, très peu
gourmands en mémoire, très rapides à lancer. Ils s'exécutent sur le même
process, donc pas besoin de s'échanger de messages pour partager des infos, ils
ont tous accès à la même zone mémoire.
Les inconvénients : n'accélèrent pas le programme. Il n'y a qu'un seul process,
donc le programme ne sera plus rapide que dans certains cas particuliers. Il
pourra même être plus lent, parce qu'il y a un besoin supplémentaire de CPU
pour gérer les coroutines.

Les avantages du parallèle : le programme s'exécute sur plusieurs process, ce
qui accélère d'autant plus les calculs, et en théorie divise la durée de ce
calcul par le nombre de process utilisés. Il permet par ailleurs de lancer le
programme sur plusieurs machines selon les langages, comme par exemple Erlang.
Les inconvénients : beaucoup plus gourmand en mémoire, beaucoup plus lourd à
gérer (lancer, synchroniser, arrêter).


Oui, d'accord, mais comment ça marche ?
---------------------------------------

Il y a différentes manières de permettre de l'exécution asynchrone, différentes
manières de faire des appels non bloquants, différents paradigmes :

- javascript : un appel asynchrone rend la main directement, et passe à la
  ligne suivante. Le résultat est ensuite récupéré par le biais d'un callback.
- clojure, go : utilisation de "canaux" pour envoyer et recevoir des messages.
  On peut imaginer ça comme des tapis roulants, avec un morceau de programme
  d'un côté qui pose des messages sur le tapis roulant, quand bon lui semble,
  et de l'autre côté un autre bout de programme qui les récupère quand bon lui
  semble. Si il n'y en a aucun, il attend. Les deux bouts de code sont donc
  désynchronisés, ils ne se bloquent pas l'un l'autre.
- python : utilisation de générateurs, appelées coroutines dans le cas de
  asyncio. On gère explicitement la boucle d'exécution.

Dans le cas de asyncio, il faut imaginer chaque "await" (ou "yield from") comme
étant le moyen pour un bout de code de dire au scheduler (à la boucle
d'exécution) : "hep, j'ai fini pour le moment, rend moi la main plus tard s'il
te plait". Ça permet à la boucle d'exécution de passer la main à d'autres bouts
de code qui ont quelque chose à faire, au lieu d'attendre séquentiellement (de
manière synchrone) que chaque bout de code se termine.


Asynchrone == plus rapide, ou pas...
------------------------------------

Mais alors, si le code s'exécute sur un seul et même process, et qu'en plus il
faut du temps de calcul pour gérer les coroutines, mon programme va être plus
lent au final ?!

Petite expérience :

En synchrone/bloquant

::

    import asyncio

    def foo():
        pass

    for i in range(10000):
        foo()

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

real    0m0.452s
user    0m0.429s
sys     0m0.019s


Donc si on fait un rapide calcul, on a environ 360ms uniquement pour la
gestion des 10000 coroutines (l'import du module asyncio, qui se fait une seule
fois au chargement du programme, a été fait dans les deux cas, histoire de ne
pas fausser les mesures).

Le but de cet exemple aberrant n'est pas de prouver que les coroutines sont
lentes (elles ne le sont pas), mais que la programmation asynchrone en
elle-même ne fait pas aller un programme plus vite (mais ça, vous vous en
doutiez).


Asyncio plus rapide pour IO-bound
---------------------------------

Mais alors, ça sert à rien asyncio ?

Laissez-moi vous conter l'histoire du programme qui attendait, parce qu'il
était bloquant.

Bob veut faire un petit programme qui va télécharger toutes les images de chat
de son site préféré. Voici un petit morceau de pseudo-code :

::

    for url in urls:
        img = get_image_from_website(url)
        thumbnail = compute_thumbnail(img)
        ...

Le programme va tour à tour télécharger les images sur le site, puis en faire
une miniature. Il y a donc deux cas différents :

- le téléchargement de l'image sur le site : on appelle ça "IO-bound",
  c'est-à-dire lié/limité par l'IO (l'input-output, entrée sortie, tout ce qui
  est un échange entre le programme et l'extérieur). Le programme va passer la
  majeure partie du temps à attendre : que la requête soit reçue par le serveur
  distant, puis traitée, puis que les données soient envoyées, puis reçues.
  Pendant tout ce temps, le programme est bloqué, et ne fait rien d'autre.
  C'est un appel bloquant.
- le calcul de la miniature : on appelle ça "CPU-bound", c'est-à-dire
  lié/limité par le CPU, par la puissance de calcul de l'ordinateur, du process
  qui fait tourner le programme. Aucune attente ici. Plus il y a de puissance
  de calcul (plus le processeur est rapide, plus il y a de CPU disponible),
  plus le programme ira vite.

Si seulement on pouvait calculer la miniature d'une image pendant le temps
d'attente du téléchargement d'une autre image ! C'est une technique connue
depuis bien longtemps dans l'industrie, le "travail en temps masqué" : pendant
qu'une machine travaille, l'employé peut faire autre chose, comme remplir le
chargeur de la machine, décharger les produits finis, lancer une autre machine,
etc...

Voilà la grande force de asyncio : pouvoir faire des appels non bloquants, pour
pouvoir faire autre chose en attendant.

Reprenons notre exemple :

En synchrone/bloquant :

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

real    0m9.722s
user    0m0.466s
sys     0m0.089s

Soit environ 10 secondes, une seconde par image.


En asynchrone/non-bloquant :

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

real    0m4.139s
user    0m0.795s
sys     0m0.094s

Soit environ 4 secondes, 0.5 seconde par image.

Plusieurs remarques :

- dans le cas du code asynchrone, il faut faire bien attention d'utiliser des
  appels non bloquants uniquement. On utilise donc aiohttp pour récupérer la
  page et l'image, puis faire les miniatures (en utilisant
  loop.run_in_executor).
- plus le code dans compute_thumbnails sera gourmand en CPU, et sera donc long
  a exécuter, plus on gagnera en performance sur la version asynchrone par
  rapport à la version synchrone, le temps de CPU étant "masqué" par le temps
  du téléchargement des pages et des images.
- le code asynchrone est plus long et complexe, et nécessite de penser le
  programme différemment.

Attention aux pièges
--------------------

::

    import asyncio
    import time

    async def foo():
        for i in range(10):
            await loop.run_in_executor(None, time.sleep, 1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(foo())

real    0m10.137s
user    0m0.079s
sys     0m0.017s

Euhhhhh, 10 secondes ? Mais pourtant, on est sensé faire les 10 appels à
time.sleep(1) en asynchrone, non bloquant, concurrent, dans des coroutines qui
vont bien et compagnie ?!

Le piège c'est que dans le code ci-dessus on exécute 10 coroutines **les unes
après les autres**.

Le code pourrait se réécrire de la façon suivante, qui met bien en valeur le
problème :

::

    import asyncio
    import time

    async def foo():
        await loop.run_in_executor(None, time.sleep, 1)

    loop = asyncio.get_event_loop()
    for i in range(10):
        loop.run_until_complete(foo())

On lance une coroutine, puis on attend qu'elle se termine avant d'en lancer une
autre. La façon correcte de l'écrire est de lancer toutes les coroutines en
même temps avec asyncio.wait() ou asyncio.gather() :

::

    import asyncio
    import time

    async def foo():
        await loop.run_in_executor(None, time.sleep, 1)

    loop = asyncio.get_event_loop()
    tasks = [foo() for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))


Asyncio est inutile pour CPU-bound
----------------------------------

La programmation asynchrone par coroutines n'est utile que pour les cas
IO-bound : lecture/écriture sur le système de fichier, sur une socket, un
serveur distant...

Il faut imaginer un process comme étant Jean-Michel CPU, employé de Prog-corp.
Le programme lui demande d'exécuter une liste de tâches. Si Jean-Michel est
déjà au taquet, réarranger les tâches, les mettre dans le désordre, bloquantes
ou non bloquantes, ne changera rien du tout.

Si par contre Jean-Michel CPU est en train de se tourner les pouces pendant que
Bernard IO est en train de trimmer à transporter des paquets de gauche et de
droite, alors on peut optimiser les choses :

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

Voilà un autre cas qui a l'air d'être IO-bound, mais en fait non :

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
programme qu'on peut écrire en python. Et donc même si en théorie une requête à
la base de donnée est de la lecture/écriture (Input-Output), dans la pratique
la réponse est tellement rapide qu'on ne peut (quasiment) rien gagner en
rendant les requêtes asynchrones. Si la base de données est distante, et que le
délai (le round-trip) est long, on peut espérer gratter un peu. Mais en général
ce n'est pas le cas (et si ça l'est, vous avez d'autres soucis à régler). Pire,
on perd le temps de la gestion des coroutines.

La programmation asynchrone est vraiment efficace et utile dans le cas de
lecture/écriture sur un système de fichier, sur une socket vers un serveur
distant... ou dans quelques autres cas notables.

Gérer des requêtes entrantes sur un serveur web de manière asynchrones grâce à
aiohttp, ou des requêtes à postgresql avec aiopg (`probablement inutile
<http://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/>`,
comme vu plus haut ?), ou avec le tout nouveau asyncpg, et plus important que
tout, télécharger des photos de chat. Voilà les exemples les plus courants
croisés dans les tutoriels.

Certains problèmes sont très pénibles à écrire de manière
synchrone/séquentielle, alors qu'ils s'expriment de manière tout à fait logique
de manière asynchrone. Par exemple un moteur de jeu : une coroutine qui gère
l'affichage en continu, et d'autres coroutines pour récupérer/traiter les
entrées du joueur.

