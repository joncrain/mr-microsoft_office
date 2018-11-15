#!/bin/sh

# Script to collect data
# and put the data into outputfile

CWD=$(dirname $0)
CACHEDIR="$CWD/cache/"
OUTPUT_FILE="${CACHEDIR}microsoft_office.txt"
SEPARATOR=' = '

# Skip manual check
if [ "$1" = 'manualcheck' ]; then
	echo 'Manual check: skipping'
	exit 0
fi

# Create cache dir if it does not exist
mkdir -p "${CACHEDIR}"

# Business logic goes here

if [ -e "/Library/Preferences/com.microsoft.office.licensingV2.plist" ]; then
	item1="vl_license"
	string1="Detected"
else
	item1="vl_license"
	string1="Not Detected"
fi
if [ -e "$HOME/Library/Group Containers/UBF8T346G9.Office/com.microsoft.Office365.plist" ]; then
	item2="365_license"
	string2="Detected"
else
	item2="365_license"
	string2="Not Detected"
fi

# Output data here
echo "$item1${SEPARATOR}$string1" > ${OUTPUT_FILE}
echo "$item2${SEPARATOR}$string2" >> ${OUTPUT_FILE}
