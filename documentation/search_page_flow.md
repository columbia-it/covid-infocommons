
Basic page loading
=====================

URL route is handled by backend/cic/urls.py
Initial (Django) render is backend/cic/views.py
Outer HTML is backend/templates/adv_search.html
React is frontend/search/src/adv_search.tsx
- note that webpack compiles adv_search.tsx into adv_search.js


Query processing
===================

When a query happens:
- react page adv_search.get_grant_data assembles the query and sends it to the backend
- backend receives it at at backend/search/views.py
  - handlers for the queries are defined by prefix in urls.py
  - in the views.py, the search_grants handler parses the query, formats it into OpenSearch format, and sends to the OpenSearch server
