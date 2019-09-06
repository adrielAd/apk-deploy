#https://stackoverflow.com/questions/23894221/upload-file-to-my-dropbox-from-python-script
import dropbox
import os
import argparse
import requests
import json
import re
def get_app(release_dir):
    '''Extract app data
    
    Args:
        release_dir (str): Path to release directory.
    Returns:
        (str, str): App version and path to release apk file.
    '''
    output_path = os.path.join(release_dir, 'output.json')

    with(open(output_path)) as app_output:
        json_data = json.load(app_output)

    apk_details_key = ''
    if 'apkInfo' in json_data[0]:
        apk_details_key = 'apkInfo'
    elif 'apkData' in json_data[0]:
        apk_details_key = 'apkData'
    else:
        print("Failed: parsing json in output file")
        return None, None

    app_version = json_data[0][apk_details_key]['versionName']
    app_file = os.path.join(release_dir, json_data[0][apk_details_key]['outputFile'])
    return app_version, app_file

def upload_file(accesstoken, file_from, file_to):
    dbx = dropbox.Dropbox(accesstoken)
    f = open(file_from, 'rb')
    dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

parser = argparse.ArgumentParser()
parser.add_argument('--release.dir', dest='release_dir', help='path to release folder', required=True)
#parser.add_argument('--app.name', dest='app_name', help='app name that will be used as file name', required=True)
parser.add_argument('--dropbox.token', dest='dropbox_token', help='dropbox access token', required=True)

options = parser.parse_args()

#access_token = 'cVdUdrCjDrAAAAAAAAAEiw4Wrk3waI8XkR66truFx-8qC8pBGbL4DM8206nBcsXV'
#file_from = options  #local file path
#file_to = '/datasend folder.webm'      # dropbox path
# Extract app version and file
app_version, app_file = get_app(options.release_dir)

appName = app_file.split("/")[-1]

name = appName.split(".")[0]
extension = appName.split(".")[1]

app_name_final = name +  "-" + app_version + "." + extension

#print(app_version)
print(appName)
print(app_name_final)
upload_file(options.dropbox_token, app_file, ("/" + app_name_final))