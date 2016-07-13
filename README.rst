Policy package
==============

``ftw.protectinactive``

.. contents:: Table of Contents

Installation local development-environment
------------------------------------------

.. code:: bash

    $ git clone git@github.com:4teamwork/ftw.protectinactive.git
    $ cd ftw.protectinactive
    $ ln -s development.cfg buildout.cfg
    $ python2.7 bootstrap.py
    $ bin/buildout
    $ bin/instance fg

Dev-Test-Release-Process
------------------------

If you want to develop features, you must follow this guide

First checkout the package and create a new branch from the master:

.. code:: bash

    $ git clone git@github.com:4teamwork/ftw.protectinactive.git
    $ cd ftw.protectinactive
    $ git checkout -b my-mew-feature
    $ git push origin -u my-new-feature

If you are finnished and the feature is working fine, you can merge it into the
master branch after the quality-check:

.. code:: bash

    $ git checkout master
    $ git merge my-mew-feature
    $ git push

Now, the feature is available for other developers.


Deployment
----------

For the deployment we use the `git-deploy <https://github.com/mislav/git-deploy>`_.

Do the following step once to setup push-deploment on the server:

`Setup git hooks on server` <https://github.com/4teamwork/plone-git-deployment#setup-git-hooks-on-server>

.. code:: bash

    gem install git-deploy
    cd the-package-repository

    git deploy setup -r production

Do the following steps on your local repo:

.. code:: bash

    # once you have to install the remotes (local)
    ./scripts/setup-git-remotes

    # deployment auf "production":
    git push production master

The push deployment will run builodut if necessary, installst plone updates and
restarts the instances.
If possible, the deployment will run without server downtime. Otherwise, it will
activate a maintenance-page.

Another example to push a local branch to a nightly installation:

.. code:: bash

    # push my local branch my-branch to the master for the nightly remote
    git push nightly my-branch:master

If you want to rerun the deployment i.e. if you just changed some versionpinnings or
if you changed src-packages without changing the master, you can run:

.. code:: bash

    git-deploy rerun -r production

For more information about push-deployment see:

`plone git deployment` <https://github.com/4teamwork/plone-git-deployment>


Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.3.9`.


Links
-----

- Github: https://github.com/4teamwork/ftw.protectinactive
- Issues: https://github.com/4teamwork/ftw.protectinactive/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.protectinactive

Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.protectinactive`` is licensed under GNU General Public License, version 2.
