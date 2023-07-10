
CIC system troubleshooting
==========================


"Lag" issue
--------------

At one point, CIC had problems with the search interface not responding to
initial queries. This behavior was erratic, and difficult to debug due to the
serverless architecture.

The root cause was simultaneous queries from the React front end to the
OpenSearch service. In the front end, the initial query and secondary "facet"
queries were fired off at the same time. Even though they were ordered in the
original code, React allowed the queries to be processed in parallel. Sometimes
the secondary queries would arrive at the search service first, and they would
not be able to complete, since the initial query had not arrived yet. These
secondary queries would block the queue and everything would stall until a 30
second timeout occurred. After that, the page would sometimes reload
automatically and sometimes need to be manually refreshed.

Reasons for the difficulty in debugging:
- Erratic behavior. The problem only occurred after the service had not been
  used for several minutes, making it difficult to reproduce on demand. This
  was likely caused by OpenSearch keeping a cache of previous queries, so
  everything would work fine until the cache would reset.
- Debugging at a "distance". The cloud/serverless architecture made it difficult
  to track the progress of individual calls through the sytem. We had to compare
  logs on the local browser with logs in the cloud system and piece together
  what was happening.

Once we understood the nature of the problem, the solution was relatively
simple: We introduced an explicit order to the queries, with a guarantee that
the initial query has been completed before the secondary queries are sent to
the OpenSearch service.
