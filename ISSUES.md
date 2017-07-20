### Critical
Fix immediately, these break functionality
* None

### General
These make functionality frustrating
* Shapes on L2 plots seem to be created but not displayed
* Persistent shapes
* There's a divide by 0 error that should be resolved in plot_depolarization
* Zoom tool is broken

### Enhancements
Add eventually, these make the program more organized and easier to use

* JSON saving/loading is kind of wonky, maybe it should be tucked away in the gui and emphasise using the database more
* Load more than 15000 profiles at once
* Could simplify plotting by creating an abstract class Plots and create a few classes PlotBackscatter(Plots), PlotVfm(Plots), etc. with all the plotting methods and displaying methods inside of them
* Clear out Vocal data block unnecessary code, other unused code

