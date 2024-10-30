import os
from boto3.session import Session
import settings

#The variable session is created using the credentials and region from the settings.py file, it includes the access key ID, the  
#secret access key and the AWS region. 
session = Session(aws_access_key_id=settings.aws_id, 
                aws_secret_access_key=settings.aws_sk, region_name=settings.aws_region)

#This function performs the download of the files from the public AWS S3 bucket to a local folder 
def download_files(bucket_name, local_directory):

    s3 = session.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    #print(paginator)
    
    for result in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in result:
            for obj in result['Contents']:
                if obj['Key'][0] == 'O':
                    key = obj['Key']
                    local_file = os.path.join(local_directory, os.path.basename(key))
                    print(local_file)
                    print(key)
                    s3.download_file(bucket_name, key, local_file)
                    print(f'Downloaded: {key} to {local_file}')

#This function simply execute the download 
def mainDownload():
    bucket_name = settings.AWS_BUTCKET
    out_path = 'Codes/Files/DownloadOutputs'
    download_files(bucket_name, out_path)
    print("The Files were download in this path: Codes/Files/DownloadOutputs")
