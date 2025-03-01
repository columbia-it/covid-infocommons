
Basic page loading
=====================

URL route is handled by backend/cic/urls.py
Initial (Django) render is backend/cic/views.py
Outer HTML is backend/templates/adv_search.html
- hands to search/main.js, which is built by webpack
- ??? not clear whether it is backend/search/static/search/main.js OR backend/static/search/main.js
React section starts at frontend/search/src/index.html and frontend/search/src/index.tsx


Query processing
===================

When a query happens:
- frontend sends it to the backend at backend/search/views.py
  - handlers for the queries are defined by prefix in urls.py
  - in the views.py, the search_grants handler parses the query, formats it into OpenSearch format, and sends to the OpenSearch server
