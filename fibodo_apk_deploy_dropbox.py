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
    
    	for root, dirs, files in os.walk(file_from):

    		#for dir_name in dirs:
    		#	print(root)
    		#	print(dir_name)

    		#try:
            #		dbx.files_create_folder(file_to, False)
            #		print("created "+ file_to + " on dropbox")
         	#except Exception as e:
            #		print("could not create dir with name", file_to)

    		for filename in files:

        		# construct the full local path
        		local_path = os.path.join(root, filename)

        		# construct the full Dropbox path
        		relative_path = os.path.relpath(local_path, file_from)
        		dropbox_path = os.path.join(file_to, relative_path)

			print(file_to)
        		#print(local_path)
        		#print(relative_path)
        		#appName = relative_path.split("/")[-1]
        		#print(appName)
        		print(dropbox_path)
			head, tail = os.path.split(dropbox_path)
			print(head)
        		try:
            			dbx.files_create_folder(head, False)
            			print("created "+ head + " on dropbox")
         		except Exception as e:
            			print("could not create dir with name", head)
        		#upload the file
        		with open(local_path, 'rb') as f:
        			dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

    

parser = argparse.ArgumentParser()
parser.add_argument('--release.dir', dest='release_dir', help='path to release folder', required=True)
parser.add_argument('--upload.dir', dest='upload_dir', help='path to upload folder in dropbox', required=True)
parser.add_argument('--dropbox.token', dest='dropbox_token', help='dropbox access token', required=True)

options = parser.parse_args()

#app_version, app_file = get_app(options.release_dir)

#appName = app_file.split("/")[-1]

#name = appName.split(".")[0]
#extension = appName.split(".")[1]

#app_name_final = name +  "-" + app_version + "." + extension

#print(appName)
#print(app_name_final)
upload_file(options.dropbox_token, options.release_dir, ("/" + options.upload_dir))