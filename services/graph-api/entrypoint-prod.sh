#!/bin/sh

echo "(prod) Waiting for neo4j..."

while ! nc -z core1 7687; do
    sleep 0.1
done

echo "Neo4j (prod) started"

gunicorn -b 0.0.0.0:5000 manage:app
