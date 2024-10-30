import json
import os
import boto3
from concurrent.futures import ThreadPoolExecutor
from botocore.exceptions import NoCredentialsError

#Global variables are declared, one for the bucket name, the other to spcify the prefix for the counter files stored in the bucket

bucket_name = 'projectpublicbucket'
counter_prefix = 'Output/'
connter_prefix_log = 'Logs/'


def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    save_log(context, s3, bucket_name, connter_prefix_log)
    for each in event:
        result(s3, each, bucket_name)
 

#This function provides the results of the processed files by accepting the S3 client, cloud file path and bucket name as parameters.
def result(s3_client, file_path, bucket_name):
    try:
        response = s3_client.get_object(Bucket='projectpublicbucket', Key=file_path)
        file_content = response['Body'].read().decode('utf-8')
        
        #evalue the operation inside the file
        result = eval(file_content) 
        #create files
        key = f'{counter_prefix}result_{os.path.basename(file_path)}'
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=str(result))

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#This function saves all the logs to the S3 bucket by accepting a parameter for the context  
def save_log(context, s3_client, bucket_name, counter_prefix_log):
    try:
        print(context)
        #Create log_info dictionary
        log_info = {
            "Lambda function ARN": context.invoked_function_arn,
            "CloudWatch log stream name": context.log_stream_name,
            "CloudWatch log group name": context.log_group_name,
            "Lambda Request ID": context.aws_request_id
        }

        #Convert the dictionary to JSON
        log_info_str = json.dumps(log_info, indent=4)

        print(log_info_str)

        #Setup key
        key = f'{counter_prefix_log}log_A_{os.path.basename(context.log_stream_name)}.txt'  # Fix the key prefix

        #Upload data to S3
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=log_info_str)

    except Exception as e:
        print(f"An error occurred while saving the log: {e}")
        #Handle the error appropriately (e.g., log it or raise an exception) 