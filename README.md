# AWS Distributed Computing


## Problem Statement:

In 2019 the current system was designed to process multiple types of
files locally, the files are first stored in Local storage eventually the
main process distributes three different types of files A, B, C into
Processes.
Now the workload has significantly increased and due to limited local
resources it takes a lot of time to process all the files sequentially,
also the solution has to go global now in 2024.
The performance of the solution can be increased by using the
concepts of Parallel and distributed systems. Public cloud provides
resources for us to process the files parallel for each type.
Therefore we would like to move our existing system to Public Cloud
in order to achieve :
- Performance
- Scalability
- Availability

### Design a Cloud Solution architecture:

Design a new system on cloud which will increase the performance of
the system, make it available and scalable in Cloud.
You will have to replace the local components with Clouds first and
eventually make the system parallel and distributed.
Hint: Use Amazon S3 for storage and AWS Lambda for Processing
Convert to Parallel and Distributed Computing in Cloud :
One of the tasks is to convert the existing system into Parallel and
Dist Computing. Here is a diagram of how the system would have
looked locally, but you will have to redesign it in the cloud.


#### S3 File Uploader ( Python ):
- Write a python program that can choose the folder to
upload on S3 and return the folder link
- Implement the functionality to download the file from S3

#### Implement the cloud Architecture:

- Functionality to Upload the files to S3 
- Implement the processing algorithms for a file locally 
- Create a Worker Lambda Function using the implemented algorithms for processing each type of files in GoLang( A, B, C ).
- Use Data from S3 in the Lambda Function
- Create a Master Lambda Function
- ( Master Lambda ) Implement functionality to distribute workload and generate new Lambda Functions
- (Worker Lambdas ) Implemented Concurrent and parrallel execution of multiple Lambda for each type of Files.
- (Worker Lambdas ) Write the Results to S3
- Save Logs from Lambda
- 
#### Script for generating new Test Cases:
Using the examples provided to you will have to create a python script to
generate at least 100 files for each type ( A, B, C ).
Input :
- N files : Number of files you would like to generate
- Type : The type of file you would like to generate

#### File Processing Algorithms:
All input files will be in .txt , the first thing you should do is generate these
files so you can test the complete system. You can use this logic to write
code to process each file type.

Type A: These files will contain mathematical equations containing whole numbers and minus, plus and division operators.

Input:
- 2 – 4
- 50 – 44
- 9 / 2
- 55 + 10

Output:
- -2
- 6
- 4.5
- 65
 
Type B: These files will contain words and you will have to reverse them.

Input:
- table
- potsdam
- me

Output:
- elbat
- madstop
- em

Type C: These files will contain binary, and you will convert them to ASCI

Input: 10001010101011010010110101100101010101 10100101110 10010101010000000001 1000110101 10110110101010101010101011111111
Output: U.5�
