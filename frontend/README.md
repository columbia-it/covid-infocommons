
CIC-E Frontend
=================

The Frontend package provides a search and viewing system for CIC-E content.

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
