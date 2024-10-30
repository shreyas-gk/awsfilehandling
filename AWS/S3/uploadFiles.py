import os
from boto3.session import Session
import settings
import json

#The variable session is created using the credentials and region from the settings.py file, it includes the access key ID, the  
#secret access key and the AWS region. 
session = Session(aws_access_key_id=settings.aws_id, 
                aws_secret_access_key=settings.aws_sk, region_name=settings.aws_region)

#This function perform the upload of the files from a local folder into the public AWS S3 Bucket 
def upload_file(bucket_name, local_file, s3_file):
    try:
        s3 = session.client('s3')
        s3.upload_file(local_file, bucket_name, s3_file)
        print(f"the file {local_file} was upload {bucket_name} as {s3_file}")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

#This function reads files from a local folder in order to get all the paths 
def read_files(folder_path, file_type):
    #Ensure the folder path ends with a separator
    if not folder_path.endswith(os.path.sep):
        folder_path += os.path.sep

    #Get a list of all files in the folder
    files = os.listdir(folder_path)
    matching_files = [file for file in files if file[0].upper() == file_type.upper()]
    return matching_files

#This function get all the apths by reading the all the files from the public AWS S3 bucket 
def read_s3Bucket(bucket_name, folder_path):
    s3 = session.client('s3')

    if not folder_path.endswith('/'):
        folder_path += '/'

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
    #print(response)
    files = [obj['Key'] for obj in response.get('Contents', [])][1:]
    
    return files    

#This function is the main entry point to upload files to the public AWS S3 Bucket. 
def mainUpload():
        bucket_name = settings.AWS_BUTCKET
        types = ['A', 'B', 'C']

        for each in types:
            listfiles = read_files(f'Codes/Files/Files_{each}', f'{each}')

            for item in listfiles:
                aws_path = f"Inputfiles/{item}"
                local_path = f"Codes/Files/Files_{each}/{item}"
                upload_file(bucket_name, local_path, aws_path)

        bucketFiles = read_s3Bucket('projectpublicbucket', 'Inputfiles/')
        lambda_client = session.client('lambda')
        function_name = 'mainLambda'

        #Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  #Use 'Event' for asynchronous invocation
            Payload=json.dumps(bucketFiles)    #If payload is needed
        )        
