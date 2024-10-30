import json
import os
import boto3
from concurrent.futures import ThreadPoolExecutor
from botocore.exceptions import NoCredentialsError

#Global variables are declared, one for the bucket name, the other to spcify the prefix for the counter files stored in the bucket
bucket_name = 'projectpublicbucket'
counter_prefix_log = 'Logs/'


#invoke the as many Worker Lambda functions as necessary concurrently for each batch of files and lastly wait for all the futures 
def lambda_handler(event, context):
    listA = []
    listB = []
    listC = []

    s3 = boto3.client('s3')
    save_log(context, s3, bucket_name, counter_prefix_log)
    for each in event:
        #print(each)
        file_type = filter(s3, each)

        if file_type == 'A':
            listA.append(each)
        elif file_type == 'B':
            listB.append(each)
        else:
            listC.append(each)
            
            
    #Split the incoming files into batches of 20 max    
    batch_size = 20
    batched_files = {
        'A': [listA[i:i + batch_size] for i in range(0, len(listA), batch_size)],
        'B': [listB[i:i + batch_size] for i in range(0, len(listB), batch_size)],
        'C': [listC[i:i + batch_size] for i in range(0, len(listC), batch_size)]
    }
 
    #Use ThreadPoolExecutor to invoke the Lambda functions concurrently
    with ThreadPoolExecutor() as executor:
        futures = []
        for file_type, batches in batched_files.items():
            for batch in batches:
                if batch:
                    futures.append(executor.submit(invoke_lambda_function, 'Worker' + file_type, batch))
 
        #Wait for all futures to complete before continuing
        for future in futures:
            future.result()

#This function invoke the workers asynchronously by accepting a parameter for the function name and the other for the payload.
def invoke_lambda_function(function_name, payload_data):
    client = boto3.client('lambda')
    
    invoke_response = client.invoke(
        FunctionName=function_name,
        InvocationType='Event',  # Asynchronous invocation
        Payload=json.dumps(payload_data),
    )
    
    return invoke_response

#This function filter all files according to their type by analyzing the content of each file by accepting a parameter for the S3
def filter(s3_client, file_path):
    try:
        response = s3_client.get_object(Bucket='projectpublicbucket', Key=file_path)
        file_content = response['Body'].read().decode('utf-8')

        resultA = any(c in ['+', '-', '*', '/'] for c in file_content)
        resultC = all(bit in {'0', '1'} for bit in file_content)

        if resultA:
            return 'A'
        elif resultC:
            return 'C'
        else:
            return 'B'

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#This function saves all the logs to the S3 bucket bz accepting a parameter for the context
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
        key = f'{counter_prefix_log}log_main_{os.path.basename(context.log_stream_name)}.txt'  #Fix the key prefix

        #Upload data to S3
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=log_info_str)

    except Exception as e:
        print(f"An error occurred while saving the log: {e}")
        # Handle the error appropriately (e.g., log it or raise an exception)

