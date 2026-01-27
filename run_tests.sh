#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running tests with coverage..."
coverage run manage.py test main

echo "Generating coverage report..."
coverage report -m

echo "Generating HTML report..."
coverage html

echo "Tests completed successfully!"
