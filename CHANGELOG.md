## Version 1.17.7
* Added ability to render Level 2 data products, including Vertical Feature Mask, Ice Water Phase, Horizontal Averaging, and Aerosol Subtype
* Added ability to select working database file, so users can now use one outside of CALIPSOdb.db in the VOCAL folder
* Fixed several bugs, including making depolarized images look more like those on the browse data site, fixed labels and titles on plots
* Added a settings dialog to manage the new config file (config.json), which allows user to switch between persistent shapes on views and default folders
* Updated documentation

### Known Issues
* Extract dialog does not work for level 2 plots

### Future Enhancements
* Draw shape of object on sidebar when clicking on selection for db
* Move database to MySQL and get away from sqlite
* Dynamic page loading for a smoother transition with panning data
* Exporting to shape files