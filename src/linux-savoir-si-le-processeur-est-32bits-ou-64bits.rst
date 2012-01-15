Linux: savoir si le processeur est 32bits ou 64bits
###################################################
:date: 2009-09-24 08:16
:category: misc
:tags: linux, systeme

Voici une astuce rapide pour savoir si le processeur d'une machine
donnée supporte le 64bits:

Il suffit de vérifier si le flag *lm* est présent dans les informations
de */proc/cpuinfo*:

::

    $ cat /proc/cpuinfo | grep lm
    flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
    pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe lm constant_tsc pebs
    bts pni monitor ds_cpl est cid cx16 xtpr lahf_lm

Le flag *lm* signifie "long mode", comme on peut le voir dans les
sources du noyau (*include/asm-i386/cpufeature.h*):

::

    #define X86_FEATURE_LM          (1*32+29) /* Long Mode (x86-64) */

Vous trouverez une liste de tous les flags sur le `blog de Nick Burch`_
(en anglais).

.. _blog de Nick Burch: http://gagravarr.livejournal.com/138575.html
