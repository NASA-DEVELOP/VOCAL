Updating The Site
=================

To build the docs, you'll need a couple of packages:

   * `graphiz`_
   * sphinx (installed with anaconda)
   * `sphinx-bootstrap-theme`_

.. note::

   This site is generated with ``sphinx`` . **do not** attempt to modify the html files of this
   site, instead refer to the :doc:`Building and Writing Docs </dev/docs>` page

The easiest way to built the site would be keeping two repositories of VOCAL active, and keep
one for developing, the other for docs. For this example the development is done on the *master*
branch, and the website will always be on the *gh-pages* branch.

.. rubric:: Cloning the Repositories

1. First, go ahead and clone two repositories into the workplace of your choice.::
   
   > mkdir vocal
   > cd vocal
   > git clone https://Github.com/Syntaf/vocal .
   > cd ..
   > mkdir docs
   > cd docs
   > git clone https://Github.com/Syntaf/vocal .

2. Now, we have two folders, your development folder ``vocal`` and your documentation site
   ``docs``. You'll need to switch the docs repository to *gh-pages*.::
   
   > cd docs
   > git checkout gh-pages

3. So you can now go on and write code, develop and create additional docs in your
   ``vocal`` workspace. When you're finally ready to rebuild the site , this will require you
   to clear your ``docs`` branch and populate it with your new generated docs.

   .. warning::

      It is **very** important you specify a directory when using the ``rm`` command. *trust me*

   .. code-block:: none

      > rm -rf docs/* 
      > cd vocal

4. Simply build the sphinx docs now with your build directory as docs!::

   > cd vocal/calipso
   > sphinx-build -b html ../docs/source ../../docs

5. Head inside your docs folder, force commit the changes and the site should be live. All done

   > cd docs
   > git push --force

.. _graphiz: http://graphviz.org/
.. _sphinx-bootstrap-theme: https://ryan-roemer.github.io/sphinx-bootstrap-theme/