=====================================
Building and Writing Docs
=====================================

One of the most important aspects of writing *good* software is clarity and readability. We hope as other developers find themselves tasked with improving this tool, documentation is also held to as high a standard as Nathan and I do.

.. rubric:: Building the docs

1. Install `sphinx`_ and `graphviz`_ [#f1]_. We use sphinx as our documentation generator, and graphviz is a visualization tool for class diagrams. 

2. Once you have these items installed, ensure you have the command ``sphinx-build`` available in your command prompt, if not you'll need to make an addition to your ``PATH``. 

3. ``cd`` to the home directory of the repository

4. Docs can be built with ``sphinx-build -b html <source-dir> <build-dir>``:: 

   > sphinx-build -b html docs/source docs/build

5. Finished! Open up index.html to view the docs, or continue reading to learn how to update to the gh-pages branch

6. ``cd`` out of your repository , and create a new folder. Inside that folder clone the repository to the current directory by specifying ``.`` at the end::

   > cd ..
   > dir
   > <DIR> CALIPSO_Visualization_tool
   > mkdir docpage
   > dir
   > <DIR> CALIPSO_Visualization_tool
   > <DIR> docpage
   > cd docpage
   > git clone <repo> .

7. Switch to the gh-pages branch inside that repo ``git checkout gh-pages``

8. Head back to the master branch repo, and build the docs specifying the build directory at the gh-pages folder. ``sphinx-build -b html docs/source ../docspage``

9. Commit and push the gh-pages branch

.. rubric:: Contributing to the Docs

The CALIPSO docs page uses the ``sphinx.ext.autodoc`` extensions to pull reStructuredText docstrings from source and create doc pages from them. inside the ``doc`` folder is the location of all code documentation, split up into three packages: *general* , *polygon* , and *tools*. If you've created a new module and would like to have it added to the docs(the answer should always be **yes**!), place a ``.rst`` file with the module name in the corresponding package folder. Inside that file you'll likely have something similar to::

   .. inheritance-diagram:: <module>

   .. py:module:: <module>

   .. automodule:: <module>
      :members:

And thats all! The documentation tool chain will do the rest for you.


.. _sphinx: http://sphinx-doc.org/
.. _graphviz: http://www.graphviz.org/
.. [#f1] You will likely need to add graphviz to your ``PATH`` once installed
