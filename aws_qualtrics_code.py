## ORG: Discriminology 
## PROJ: Discriminology AWS & VOW Qualtrics Data Connection
## cODERS: Robb K.
## OPEN: December 2022
## CLOSE: March 2023

## OBJ: Create a safe, secure system to transition VOW Qualtrics survey data for CACS over to Discriminology's AWS database storage account so data can be
## pushed to Discriminology+ for analyzing and insights. 

## HAT-TIPS##
## https://www.youtube.com/watch?v=_uhY_a4NgNc
## https://gist.github.com/FedericoTartarini/9496282b4b2f508c0ab2da96f4955397
## https://medium.com/bilesanmiahmad/how-to-upload-a-file-to-amazon-s3-in-python-68757a1867c6


## Install necessary packages 
## Note: Only open this code if the packages are not already uploaded
#import sys
#!{sys.executable} -m pip install requests
#!{sys.executable} -m pip install zipfile
#!{sys.executable} -m pip install io
#!{sys.executable} -m pip install pandas
#!{sys.executable} -m pip install boto3


## Import the packages needed to run the code
import requests
import zipfile
import io
from urllib.request import urlopen
from io import TextIOWrapper
import csv
import pandas as pd
from datetime import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError

## This information is needed to access VOW's Qualtrics account data
ACCESS_KEY = 'AKIAU3AZCM4EHDHUBY6Z'
SECRET_KEY = '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'


## Define function to send qualtrics data to amazon s3 bucket:
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_fileobj(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


## Define get_qualtrics_survey(dir_save_survey, survey_id):
def get_qualtrics_survey(survey_id):
    """ automatically query the qualtrics survey data
    guide https://community.alteryx.com/t5/Alteryx-Designer-Discussions/Python-Tool-Downloading-Qualtrics-Survey-Data-using-Python-API/td-p/304898 """

    ## Setting user Parameters
    api_token = "B8zJdWTFUxIG7zHLsL0z3ARb4hA6k6SMpCGIHGbb"
    file_format = "csv"
    data_center = 'villageofwisdom.iad1' # "<Organization ID>.<Datacenter ID>"

    ## Setting static parameters
    request_check_progress = 0
    progress_status = "in progress"
    base_url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
    headers = {
        "content-type": "application/json",
        "x-api-token": api_token,
    }

    ## Step 1: Creating Data Export
    download_request_url = base_url
    download_request_payload = '{"format":"' + file_format + '","surveyId":"' + survey_id + '"}' # you can set useLabels:True to get responses in text format
    download_request_response = requests.request("POST", download_request_url, data=download_request_payload, headers=headers)
    progress_id = download_request_response.json()["result"]["id"]

    ## Step 2: Checking on Data Export Progress and waiting until export is ready
    while request_check_progress < 100 and progress_status != "complete":
        request_check_url = base_url + progress_id
        request_check_response = requests.request("GET", request_check_url, headers=headers)
        request_check_progress = request_check_response.json()["result"]["percentComplete"]

    ## Step 3: Downloading file
    request_download_url = base_url + progress_id + '/file'
    request_download = requests.request("GET", request_download_url, headers=headers, stream=True)

    ## Step 4: Unzipping the file        
    survey_name = zipfile.ZipFile(io.BytesIO(request_download.content)).namelist()[0]
    with zipfile.ZipFile(io.BytesIO(request_download.content)).open("{0}".format(survey_name)) as myfile:                
        ## Note: Only open this for code testing purposes
        #df = pd.read_csv(myfile) 
        #return df
        
        uploaded = upload_to_aws(myfile, 'vow-qualtrics-cacs', 'vow_qualtrics'+str(datetime.now()))
        return uploaded
    
    
## Get survey results
get_qualtrics_survey(survey_id = 'SV_9tLguY6hRS2yqns')
