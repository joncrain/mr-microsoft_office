#!/bin/bash

# microsoft_office controller
CTL="${BASEURL}index.php?/module/microsoft_office/"

# Get the scripts in the proper directories
${CURL} "${CTL}get_script/microsoft_office.sh" -o "${MUNKIPATH}preflight.d/microsoft_office.sh"

# Check exit status of curl
if [ $? = 0 ]; then
	# Make executable
	chmod a+x "${MUNKIPATH}preflight.d/microsoft_office.sh"

	# Set preference to include this file in the preflight check
	setreportpref "microsoft_office" "${CACHEPATH}microsoft_office.txt"

else
	echo "Failed to download all required components!"
	rm -f "${MUNKIPATH}preflight.d/microsoft_office.sh"

	# Signal that we had an error
	ERR=1
fi
