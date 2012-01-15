django et le handler500: retourner une erreur 503
#################################################
:date: 2011-04-14 17:04
:category: django

Une mise en production ratée ? Un (local) settings oublié ? Un bug
inconnu jusqu'alors ?

Dans les trois cas cités, il y a de fortes chances pour que vos
utilisateurs voient une erreur 500 (*internal server error* : erreur
interne du serveur). Il est facile, en peaufinant son template
*500.html* d'afficher un message d'erreur sympatique à l'utilisateur,
pour lui expliquer qu'il suffit de patienter, que vous êtes sur la
brèche, et que ce bug est en cours de résolution!

En effet, votre serveur de production n'étant pas en *DEBUG = True*
(hein, rassurez-moi), et si vous avez conservé le mécanisme par défaut
de django qui vous notifie des erreurs 500 par mail, vous êtes déjà au
courant du soucis.

Seulement, si un *crawl bot* (robot indexeur) passe par là, il va
tomber sur une page (ou plusieurs) qui ne fonctionne(nt) pas. Je ne sais
pas quel est l'impact sur le classement de votre site, mais ce qui est
sûr, c'est que ce genre d'erreur (ainsi que les erreurs 4xx) ne peut
avoir qu'un impact négatif.

Heureusement, il existe le code d'erreur 503 (*service unavailable* :
service indisponible) qui permet de spécifier un header *Retry-After*
(réessayer après), avec une durée ou une date.

Voici comment détourner le *handler500* fournit par défaut par django,
pour renvoyer un code d'erreur 503, et le *header* associé, dans notre
cas, un *Retry-After* d'une heure :

Créer son propre handler
~~~~~~~~~~~~~~~~~~~~~~~~

Pour celà, créer par exemple le fichier *utils/handlers.py* :

::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from django import http
    from django.views.decorators.csrf import requires_csrf_token
    from django.template import Context, loader

    class MyHttpResponseServerError(http.HttpResponse):
        status_code = 503

        def __init__(self, *args, **kwargs):
            http.HttpResponse.__init__(self, *args, **kwargs)
            self['Retry-After'] = '3600'

    @requires_csrf_token
    def handler500(request, template_name='500.html'):
        """Error handler that returns a 503 status code and a Retry-After header.

        Returning a 503 error code will tell crawl bots to retry later.

        """
        t = loader.get_template(template_name)
        return MyHttpResponseServerError(t.render(Context({})))

Détourner le handler500 par défaut
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Et maintenant, il suffit de spécifier dans son *ROOT URLCONF* (le
fichier *urls.py* à la racine du projet) :

::

    handler500 = 'utils.handlers.handler500'

Conclusion
~~~~~~~~~~

Il est difficile de savoir si retourner un statut 503 est préférable à
un statut 500, en particulier sur le *ranking* dans les moteurs de
recherche. Il y a bien `une réponse`_ (approchante) d'un employé de
Google qui laisse penser qu'un 503 est recommandé.
Dans tous les cas, je trouve plus sympa et propre d'avoir une erreur
indiquant clairement que c'est un soucis temporaire, avec un ordre
d'idée du délai avant de réessayer de visiter cette url.

Qu'en pensez-vous?

.. _une réponse: http://groups.google.com/group/google_webmaster_help-indexing/msg/bc49ca084f7e79c7
