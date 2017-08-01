## Version 1.17.8
* Added ability to render Level 2 data products, including Vertical Feature Mask, Ice Water Phase, Horizontal Averaging, and Aerosol Subtype
* Added ability to select working database file, so users can now use one outside of CALIPSOdb.db in the VOCAL folder
* Added a settings dialog to manage the new config file (config.json), which allows user to switch between persistent shapes on views and default folders
* Fixed several bugs, including making depolarized images look more like those on the browse data site, fixed labels and titles on plots
* Changed free draw tool so that it creates a "rubberband", or temporary line, to follow the cursor before the next point is plotted
* Updated documentation

### Known Issues
* Extract dialog does not work for level 2 plots
* Magnify tool does not work

### Future Enhancements
* Draw shape of object on sidebar when clicking on selection for db
* Move database to MySQL and get away from sqlite
* Dynamic page loading for a smoother transition with panning data
* Exporting to shape files