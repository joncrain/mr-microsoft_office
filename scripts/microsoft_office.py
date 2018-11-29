#!/usr/bin/python
import plistlib
import os
import subprocess
import sys
import json
import CoreFoundation
sys.path.insert(0, '/usr/local/munki')
from munkilib import FoundationPlist

DEBUG = False

# Don't skip manual check
if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        print '**** DEBUGGING ENABLED ****'
        DEBUG = True
        import pprint
        PP = pprint.PrettyPrinter(indent=4)

microsoft_office_config = {}

# Apps to check
apps=['Microsoft Word','Microsoft Excel','Microsoft Outlook','Microsoft PowerPoint','Microsoft OneNote','Microsoft Teams','OneDrive']
for app in apps:
    app_path = '/Applications/' + app + '.app/'
    if os.path.isdir(app_path):
        microsoft_office_config[app] = {}
        if os.path.exists(app_path + '/Contents/_MASReceipt'):
            microsoft_office_config[app]["MAS"] = "True"
        else:
            microsoft_office_config[app]["MAS"] = "False"
        pl = FoundationPlist.readPlist(app_path + '/Contents/Info.plist')
        app_version = pl["CFBundleVersion"]
        microsoft_office_config[app]["Version"] = app_version

# Check for Licensing Helper file
Licensing_Helper = os.path.isfile("/Library/PrivilegedHelperTools/com.microsoft.office.licensingV2.helper")
if Licensing_Helper:
    microsoft_office_config['Licensing_Helper'] = 'Detected'
else:
    microsoft_office_config['Licensing_Helper'] = 'Not Detected'

# Check for Retail VL License
Retail_VL_License = os.path.isfile("/Library/Preferences/com.microsoft.office.licensingV2.plist")
if Retail_VL_License:
    microsoft_office_config['Retail_VL_License'] = 'Detected'
else:
    microsoft_office_config['Retail_VL_License'] = 'Not Detected'

# Check versions for each app

# Check MAS for each app

# Get all users' home folders
cmd = ['dscl', '.', '-readall', '/Users', 'NFSHomeDirectory']
proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(output, unused_error) = proc.communicate()

# Check each home folder for MAU Channel
for user in output.split('\n'):
    if 'NFSHomeDirectory' in user and '/var/empty' not in user:
        user_name = user.replace("NFSHomeDirectory: /Users/", "")
        userpath = user.replace("NFSHomeDirectory: ", "")
        # Check each home folder for MAU Version
        autoupdate_pref = userpath + '/Library/Preferences/com.microsoft.autoupdate2.plist'
        if os.path.isfile(autoupdate_pref):
            pl = FoundationPlist.readPlist(autoupdate_pref)
            microsoft_office_config["Users"] = {}
            microsoft_office_config["Users"][user_name] = {}
            microsoft_office_config["Users"][user_name]["MAU_Channel"] = pl["ChannelName"]
        # Check each home folder for Office 365 License
        office_365_license = userpath + '/Library/Group Containers/UBF8T346G9.Office/com.microsoft.Office365.plist'
        if os.path.isfile(office_365_license):
            microsoft_office_config["Users"][user_name]["Office_365_License"] = "Detected"

def main():
    """Main"""
    # Create cache dir if it does not exist
    cachedir = '%s/cache' % os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    microsoft_office_cache = os.path.join(cachedir, 'microsoft_office.json')

    print json.dumps(microsoft_office_config, indent=4)
    with open(microsoft_office_cache, 'w') as fp:
        json.dump(microsoft_office_config, fp, indent=4)


if __name__ == "__main__":
    main()
