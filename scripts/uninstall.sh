#!/bin/bash

# Remove microsoft_office script
rm -f "${MUNKIPATH}preflight.d/microsoft_office.py"

# Remove microsoft_office.txt file
rm -f "${MUNKIPATH}preflight.d/cache/microsoft_office.json"
