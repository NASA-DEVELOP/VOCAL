### Critical
Fix before immediately, breaks functionality

- None

### General
Fix before push to master, makes functionality frustrating

- Shapes on L2 plots seem to be created but not displayed

- There's a divide by 0 error that should be resolved in plot_depolarization

- There is a horizontal division in the backscatter render

- Zoom tool is broken

### Enhancements
Add eventually, makes the program more organized and easier to use

- Load more than 15000 profiles at once

- Could simplify plotting by creating an abstract class Plots and create a few classes PlotBackscatter(Plots), PlotVfm(Plots), etc. with all the plotting methods and displaying methods inside of them

- Make the plot selection menu more intuitive

- Clear out Vocal data block unnecessary code, other unused code