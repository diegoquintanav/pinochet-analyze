#!/bin/sh

echo "Waiting for neo4j..."

while ! nc -z core1 7687; do
  sleep 0.1
done

echo "Neo4j started"

python manage.py run -h 0.0.0.0
