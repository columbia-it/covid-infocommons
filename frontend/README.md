
CIC-E Frontend
=================

The Frontend package provides a search and viewing system for CIC-E content. It is based on React and Material UI. 

Installation
=================

These steps will update the files used by the frontend system, and
upload them to a location that can be referenced by Django:
- npm install
- python manage.py collectstatic
- npm run webpack

Note that this does not start a server! When users access the (backend) Django server,
it will give them the frontend files, which will run in their local browser. 


Search UI
=============

The Search UI

The UI currently searches over grant fields 'title', 'abstract', 'award_id', 'keywords'


Styling
========

The stylesheet in `frontend/src/main.css` is the primary stylesheet
for the site. When running `npm webpack`, the stylesheet is copied to
the appropriate backend location.

Items that are within the React components are styled with the
`emotion/react` toolkit.
- HTML elements within React can be assigned
  a `className` attribute, and this will be converted into a `class`
  that may be styled by the `main.css`. However, in many cases, other
  parts of Material UI will override these styles.
