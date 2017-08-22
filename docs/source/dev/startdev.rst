Getting Started Developing
==========================

Before writing your first line of code in VOCAL, give the user and developer documentation a read
through!

--------------
Learn the Code
--------------

Make sure your python skills are up to date. Check out the `Code Academy`__ website for an interactive
python tutorial. Refer to the `python 2.7 documentation`__ for help with specific commands. We also recommend `introductory programming lessons`__ on the Command Line, Git, and Python developed by Software Carpentry. VOCAL is
based heavily on Tk/Tkinter. Documetaion and examples can be found on a multitude of sites, but
`Effbot`__ has some good examples and explanations. Finally, check out the GitHub to see VOCAL's
`repository`__. Try looking through the code to get a feeling for the flow and organization of the
program before you start making additions.

------------
Get in Touch
------------

Many DEVELOPers have put their hands on VOCAL's code and can provide you with some great insight into
how the program is structured and what challenges they faced. Join the Slack or just send an email
to one of the previous project leads.

-------
Use Git
-------

Before you start making changes, learn how to use Git for version control. GitHub provides an
`interactive tutorial`__ on using Git, but there a resources all over the web. We really recommend this Software Carpentry tutorial, `Version Control with Git`__. For VOCAL, we stick
to several best practices in order to streamline development. If you plan on developing VOCAL, you
**must** use Git.

Software for Developing
#######################

The IDE, Debugger, or text editor you use are all up to you , as long as you use Git. Pycharm is a
great IDE with debugging, syntax highlighting, formatting suggestions, and Git capabilities. You can
grab the free community version from their website `here`__. If you prefer a more basic environment,
you can always use your favorite text editor (`Sublime Text`__ is a great option) along with
`Gitbash`__ to interact with the GitHub repository.

Clone the Repository
####################

If you plan on using an IDE or debugging software, then simply follow the directions provided by
their documentation to clone from GitHub. Make sure you select the Anaconda python 2.7 version as
your compiler.

Otherwise, you can use Git Bash to clone the repository.

1. First, open Git Bash

   * Use ``cd`` to reach the folder where you would like to develop VOCAL

2. Then use ``git clone https://github.com/NASA-DEVELOP/VOCAL.git``

   * ``git fetch`` to make sure the branches are up to date

3. To start VOCAL, use ``python VOCAL/calipso/Calipso.py``

Start Developing
################

To begin developing, you will need a new branch.

  .. warning::
     **never** update the master branch directly unless you are making small changes or it is
     absolutly necessary.

1. Use ``git checkout -b newbranch`` to create a branch called *newbranch*

   * You should choose a more relevant name, such as the number of the issue you are fixing or
     the name of the feature you are adding

   * If you are using an IDE, use their tools to create a new local repository. In Pycharm, you can
     right-click the project folder and use Git > Repository > Branches > New Branch

2. You are now free to develop the python files within VOCAL. Before you start, make sure you read
   the rest of the user and developer documentation, **especially** the
   :doc:`coding conventions <dev/conventions>`. Write lots of comments, keep track of the changes
   you make in the changelog, and be ready to explain any code to future developers

3. When you have made some progress on your branch, you should save and commit the changes.

   * If you created new files, use ``git add newfile`` to add the file *newfile*. Similarly, use
     ``git rm oldfile`` to remove a file called *oldfile*

   * Otherwise, use ``git commit -m  "Your commit message here"`` to commit changes to your
     branch with a short message

     * To make commits on Pycharm, right-click the project folder and select Git > Commit Directory

   * Git will keep track of your changes from one commit to another and allows you to revert if you
     mess something up. Checkout tutorials online for a more in depth guide on using Git and all of the features it offers.

4. When you make big commits or after a few small ones, you should upload your commits to the GitHub

   * Use ``git push origin newbranch`` (replace *newbranch* with the name of your branch)

After you work on your branch for a while and find that your changes have not cause any further
errors, you can merge it back into the master

Merging a Branch
################

After you have made updates or fixed bugs on your own branch, you can merge it back into the master.
make sure your files are saved and you latest commit is up to date.

1. Head over to the GitHub page on your web browser and select your branch from the list. Then click *New Pull Request*

2. You will be prompted to write a message to accompany the request. Write in your changes and any
   other relevant information such as known bugs. Then submit the request.

3. There may be conflicts with the two branches, so resolve those on the GitHub gui before you merge

4. Once you've had another person look over your pull request and it looks good, confirm the merge.

VOCAL's master branch is now up to date with yours. Once some more people have tested the new master
branch, go ahead and delete the *newbranch* that you created earlier. All of the changes you made are
on the master branch now, so you won't need it anymore

-----------
Closing Out
-----------

At the end of your session, you should do a few things to make development easier for the next team.

1. Make sure all of your changes have been uploaded to the GitHub with good comments. Someone new
   should be able to come along and figure out what the code is supposed to do pretty easily.

2. Update the documentation considering the updates you made. If you added or removed features, note
   them in the changelog and make sure the docs explain the feature accurately. Update the contact info
   in the documentation and the about in the constants.py file.

3. If you leave behind any unfinished features or code, leave detailed guides on what you attempted
   and the goal of the code so the next team can either finish it or scrap it quickly.

Versioning
##########

If you believe that the changes you have made to VOCAL constitute a new version, it should be named *1.YY.MM* where *YY* is the year of the release and *MM* is the month. VOCAL 2 will be deployed as a web app.



.. __: https://www.codecademy.com/
.. __: https://docs.python.org/2/
.. __: https://software-carpentry.org/lessons/
.. __: http://effbot.org/tkinterbook/
.. __: https://github.com/NASA-DEVELOP/VOCAL
.. __: https://try.github.io/levels/1/challenges/1
.. __: swcarpentry.github.io/git-novice/
.. __: https://www.jetbrains.com/pycharm/
.. __: https://www.sublimetext.com/
.. __: https://git-scm.com/downloads
