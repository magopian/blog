VIM et la correction orthographique
###################################
:date: 2012-02-28 09:44
:category: misc

Si vous ne le saviez pas déjà, VIM possède un correcteur orthographique dans le style de "Myspell" (utilisé aussi par la suite OpenOffice/LibreOffice ainsi que par Mozilla).

La documentation est disponible ici : http://vimdoc.sourceforge.net/htmldoc/spell.html


Ajouter le dictionnaire français
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour l'activer :

.. code-block:: vim

    :setlocal spell spelllang=fr

Si le dictionnaire n'est pas déjà présent, il sera automatiquement téléchargé pour vous, facile ! Attention néanmoins, vérifiez bien que la locale "fr_FR.utf8" est installée ET qu'elle est celle activée par défaut :

.. code-block:: sh

    locale -a  # doit lister fr_FR.utf8, sinon la créer
    locale  # doit lister LANG=fr_FR.utf8

Pour créer une locale, veuillez vous reporter à la documentation de votre distribution (par exemple https://wiki.archlinux.org/index.php/Locale#Enabling_necessary_locales).

Afin que le dictionnaire puisse être téléchargé et configuré, la langue *fr* doit obligatoirement être la langue courante. Pour l'activer temporairement, juste pour le téléchargement et la configuration :

.. code-block:: sh

    export LANG=fr_FR.utf8
    vim  # puis :setlocal spell spelllang=fr


Raccourcis pratiques
~~~~~~~~~~~~~~~~~~~~

Pour activer ou désactiver le correcteur orthographique (*toggle*), et pouvoir basculer rapidement entre les langues *fr* et *en*, il suffit de rajouter deux touches de raccourci au choix dans son ``.vimrc`` :

.. code-block:: vim

    " spell checking
    function! ToggleSpellLang()
        " toggle between en and fr
        if &spelllang =~# 'en'
            :set spelllang=fr
        else
            :set spelllang=en
        endif
    endfunction
    nnoremap <F7> :setlocal spell!<CR> " toggle spell on or off
    nnoremap <F8> :call ToggleSpellLang()<CR> " toggle language
