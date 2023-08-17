# Changelog

## v0.1.1 (2020-09-08)

### New

- Finish basic endpoints in graphql. [Diego Quintana]

  no tests, except one lame thingy I did in schemas.py

- Implement primary keys in nodes. [Diego Quintana]

- Neo4j models and graph seeding implemented. [Diego Quintana]

- Add basic Victim model and schema, queryable from graphql. [Diego Quintana]

  not tested, this needs tests!

- Add a modeling notebook that creates Victim instances in neo4j. [Diego Quintana]

  also modify docker-compose to incorporate links between apoc and data

- Add a docker instance with a neo4j empty database. [Diego Quintana]

- Add versioning utilities like gitchangelog, precommit, black and other goodies. [Diego Quintana]

### Changes

- Bridge datetime objects from csv to graphql. [Diego Quintana]

  this is monkey patching the py2neo and graphene apis that do not
  support datetime objects as they should

  - py2neo does not support datatype schemas, although it performs
  conversions internally
  - py2neo matches objects into neotime objects
  - graphene does not know how to read neotime objects

  I will try using node.js next time

- Restructuration of folders, because experience. [Diego Quintana]

  also, update Pipfile dependencies to reach a stable point

### Fix

- Update models and loading script. [Diego Quintana]

  this removes customproperty and updates the loading script
  to consider the new column names in
  <https://github.com/danilofreire/pinochet/issues/3>

  It also swaps the order between event and location in the graph
  definition. It was not working but some magic happened and now it
  does.

- Fix relationship IN_LOCATION not set for all locations. [Diego Quintana]

### Other

- Add pytest. [Diego Quintana]

- Fix poor implementation of app at manage.py. [Diego Quintana]

  see https://github.com/pallets/flask/issues/3701 for details

- Dev: new: implement setup.py and a better configuration handling. [Diego Quintana]

- Update neo4j models and implement CLI methods in manage.py. [Diego Quintana]

- Update docs with the full rettig report. [Diego Quintana]

- Update modeling notebooks with violentEvent schema. [Diego Quintana]



## v0.1.0 (2020-07-04)

### New

- Add shiny badge with python version in use. [Diego Quintana]

- Add Pipfile and Pipfile.lock. Let's see what this is about. [Diego Quintana]

- Add a container to serve the map with nginx :tada: [Diego Quintana]

  Launch it with docker-compose up -d, and check 0.0.0.0

- Add LICENSE and README. [Diego Quintana]

### Changes

- Update maps, search boxes, hover, etc. [Diego Quintana]

  Better usage of the folium API. There are some things still pending.
