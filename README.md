## Docs:

http://develop-larc-calipso.github.io/CALIPSO_Visualization/

## To-Do:

* [x] Fix bug : zoom remains toggled when switching from free draw to zoom
* [x] Fix naming conventions of code
* [ ] JSON writer and reader
  * [x] JSON writer
  * [x] JSON reader
* [ ] Add attributes to polygon objects
* [x] Show plot coordinates in lower left hand corner of screen
* [x] Discuss global variable `toggleContainer`
* [ ] Make shapes not fill in when `focus` is toggled
* [ ] Add docs for JSON writer / reader
* [x] Create more efficient manner of generating toolbar buttons
* [x] Fix JSON parsing empty objects
* [x] Fix JSON not storing free draw shapes
* [x] Add popup window for JSON creation
* [x] Fix coordinate system displayed on matplotlib backend
* [ ] Update drag functionality
* [x] Rewrite `polygonWriter`
* [ ] Rewrite docs
* [ ] Round vertices to a nearest decimal place
* [ ] move vertices to plot points

## Experimental To-Do:

* [x] Create dialog for listing database objects
  * [ ] Introduce filtering of objects
* [ ] Do not add objects already placed inside the database
* [ ] Do not duplicate objects that have not moved from the database
* [ ] Add warning on corrupted objects (nan)
* [x] Move exporting of data to DB to the menu bar
* [x] Remove save function button
* [x] Create some sort of DB monitoring system to catch empty and bad objects
* [ ] Inside import dialog give ability to delete
