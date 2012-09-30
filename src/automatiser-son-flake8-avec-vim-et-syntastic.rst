Automatiser son flake8 avec vim et syntastic
############################################
:date: 2012-09-30 11:40
:category: django

Toi, ami développeur Python, j'espère que tu connais déjà flake8_. Flake8 te
permet de valider en une seule fois que ton code Python est propre au regard de
pep8_ et de pyflakes_.

Si tu ne connais aucun des trois programmes que je viens de nommer, et que tu
n'utilise pas non plus pylint_, je pense qu'il est temps pour toi d'arrêter de
lire cet article, et de te documenter. Au plus vite. Non, en fait, maintenant,
là, tout de suite.

Pour les têtes dures, ces utilitaires permettent de valider que le code est
compatible avec la `pep 0008`_, qu'il n'y a pas d'erreur de syntaxe, d'import
ou de variable inutilisés, etc...

Ils permettent donc d'être sûrs de la qualité de la mise en forme du code (et
malheureusement pas de la qualité du code lui-même). Si quelqu'un connaît un
outil qui permette de faire ça, je suis preneur : il y a bien `l'indice de
complexité de McCabe`_ (qui peut être fournie par ``flake8``), mais il ne
permet pas de mesurer la qualité totale d'un code. J'imagine que c'est trop
subjectif pour être mesuré objectivement.


Je suis trop fainéant
=====================

C'est très bien, d'être fainéant. Être fainéant, c'est vouloir se simplifier la
vie, en obtenir plus en travaillant moins, c'est un `noble but`_.

Et je dois avouer que lancer à la main ``pep8`` puis ``pyflakes`` (j'utilisais
en fait déjà un `plugin Vim pour pyflakes`_) régulièrement, puis retourner sur
le code qu'on pensait avoir fini pour le nettoyer, retrouver la ligne
correspondante à chaque erreur, c'était fastidieux.

Flake8 permet de récupérer les erreurs de ``pep8`` et de ``pyflakes`` en une
seule fois, ce qui est déjà une amélioration. Mais ce n'est pas suffisant, il
reste toujours à le lancer manuellement...


Syntastic à notre secours
=========================

C'est là qu'intervient notre sauveur : syntastic_.

Il s'installe en un tournemain avec pathogen_, que vous devriez utiliser (non,
ce n'est pas un conseil, c'est un ordre).

La doc d'installation de ``syntastic`` est limpide, et si vous avez ``flake8``
installé, vous n'avez rien d'autre à faire ! En fait, ``syntastic`` va
utiliser le premier exécutable qu'il trouve parmi ``flake8``, ``pyflakes`` et
``pylint``.

Une fois ``syntastic`` installé, à chaque sauvegarde de votre fichier, vous
verrez une marque apparaître dans la marge de gauche pour chaque violation de
règle de formatage.

Il n'y a donc plus aucune raison pour ne pas valider ton code ! Fais toi une
faveur, ainsi qu'à ceux qui devront relire ta prose.

----


.. target-notes::

.. _flake8: https://bitbucket.org/tarek/flake8
.. _pep8: https://github.com/jcrocholl/pep8/
.. _pyflakes: https://launchpad.net/pyflakes
.. _pylint: http://www.logilab.org/project/pylint
.. _pep 0008: http://www.python.org/dev/peps/pep-0008/
.. _l'indice de complexité de McCabe: https://fr.wikipedia.org/wiki/Nombre_cyclomatique
.. _noble but: http://agopian.info/djangocong/dplf.html
.. _plugin Vim pour pyflakes: http://www.vim.org/scripts/script.php?script_id=2441
.. _syntastic: https://github.com/scrooloose/syntastic
.. _pathogen: https://github.com/tpope/vim-pathogen
