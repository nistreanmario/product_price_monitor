#!/bin/bash

echo "Running entrypoint.sh:"

echo "Applying migrations"
python manage.py migrate

echo "Done entrypoint.sh"
exec "$@"
