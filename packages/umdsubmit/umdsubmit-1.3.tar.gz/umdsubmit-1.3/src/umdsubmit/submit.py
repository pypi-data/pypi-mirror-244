import os
import requests
import shutil
import getpass

def get_info(lineStart):
    f = open(".submit", "r")
    for line in f:
        if line.startswith(lineStart):
            k, v = line.split('=')
            return v.strip()

def get_cvs_account():
    if os.path.isfile(".submitUser"):
        f = open(".submitUser", "r")
        for line in f:
            if line.startswith('cvsAccount'):
                k, v = line.split('=')
                return v.strip()
    else:
        auth()
        return get_cvs_account()

def get_one_time_password():
    if os.path.isfile(".submitUser"):
        f = open(".submitUser", "r")
        for line in f:
            if line.startswith('oneTimePassword'):
                k, v = line.split('=')
                return v.strip()
    else:
        auth()
        return get_one_time_password()

def walk_and_add_files(zip_writer):
    for folder, _, files in os.walk("."):
        for file in files:

            if file != ".submitUser":
                file_path = os.path.join(folder, file)
                with open(file_path, "rb") as f:
                    zip_writer.writestr(file_path, f.read())

def auth():
    print("Enter UMD Directory ID: ")
    username = input()
    password = getpass.getpass("Enter UMD Password: ")
    data = {"loginName" : username, "password" : password, "courseKey" : get_info("courseKey"), "projectNumber" : get_info("projectNumber")}
    url_part = f"/eclipse/NegotiateOneTimePassword"
    response = requests.post(get_info("baseURL") + url_part, data = data)
    f = open(".submitUser", "x")
    f.write(response.text)
    print(response.text)

def main():
    
    shutil.make_archive('submit', 'zip', os.getcwd())
    
    
    submit_zip_object =  open('submit.zip', 'rb')
    files = {"submittedFiles": ("submit.zip", submit_zip_object)}
    
    
    
    data = {"courseName" : get_info("courseName"), "projectNumber" : get_info("projectNumber"), "semester" : get_info("semester"), "courseKey" : get_info("courseKey"), "authentication.type" : get_info("authentication.type"), "baseURL" : get_info("baseURL"), "submitURL" : get_info("submitURL"), "cvsAccount" : get_cvs_account(), "oneTimePassword" : get_one_time_password(), "submitClientTool" : "umdsubmit", "submitClientVersion" : "1.0"}
    response = requests.post(get_info("submitURL"), files = files, data = data)
    print(response.text)
