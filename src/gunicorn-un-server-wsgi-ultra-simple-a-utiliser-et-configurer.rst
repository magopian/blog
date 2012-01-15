gunicorn: un server wsgi ultra simple à utiliser et configurer
##############################################################
:date: 2010-02-09 17:08
:category: django

Deux billets le même jour, c'est fête!

Voici une recette simple pour installer, configurer et utiliser
`gunicorn`_ avec `apache`_ et `django`_.

Installer gunicorn
~~~~~~~~~~~~~~~~~~

Pour installer gunicorn dans son environnement virtuel:

::

    $ pip install -E /path/to/venv install gunicorn

Configurer Apache en proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~

Apache servira les fichiers statiques, et "proxisera" toutes les autres
requêtes directement à gunicorn qui sera lancé en local sur le port
8080:

::

    <VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com

    DocumentRoot /path/to/django/project

    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>

    # laisser apache servir les fichiers statiques
    ProxyPass /robots.txt !
    ProxyPass /favicon.ico !
    ProxyPass /static/ !

    # proxiser toutes les autres requêtes vers gunicorn
    ProxyPass / http://localhost:8080/

    # robots.txt et favicon.ico sont dans /path/to/django/project/static/
    Alias /robots.txt /path/to/django/project/static/robots.txt
    Alias /favicon.ico /path/to/django/project/static/favicon.ico

    <Directory /path/to/django/project>
        Order deny,allow
        Allow from all
        Options -Indexes
    </Directory>
    </VirtualHost>

Pour que le tout fonctionne correctement, il faut activer les modules
*mod\_proxy* et *mod\_proxy\_html* (et en option *mod\_cache*):

::

    $ a2enmod proxy proxy_http cache

Puis de redémarrer le server Apache:

::

    $ /etc/init.d/apache2 restart

Lancer gunicorn
~~~~~~~~~~~~~~~

Il suffit de se placer dans le répertoire du projet django (avec le
virtualenv activé), puis de taper:

::

    $ gunicorn_django -b localhost:8080 --workers=2

Un ordre d'idée pour le calcul des *workers*: un de plus que le nombre
de CPUs de la machine.

Conclusion
~~~~~~~~~~

On peut alors se créer un script (a placer dans /etc/init.d) et
l'activer pour qu'il se lance automatiquement au démarrage avec la
commande *update-rc.d* (sous Debian), ou utiliser `runit`_ (jamais
testé, peut-être un futur billet?).

Encore mieux, remplacer Apache par Nginx! (jamais testé non plus, et
sûrement un futur billet ;)).

On peut difficilement faire plus simple!

.. _gunicorn: http://github.com/benoitc/gunicorn
.. _apache: http://www.apache.org/
.. _django: http://www.djangoproject.com/
.. _runit: http://smarden.org/runit/
