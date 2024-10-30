#This file acts as the "interface", hence why it imports other files like the GeneratorMain.py, 
#the uploaderFiles.py and the downloadFiles.py which are pretty self explanatory
from Codes.Generator.GeneratorMain import mainGenerator
from Codes.AWS.S3.uploadFiles import mainUpload
from Codes.AWS.S3.downloadFiles import mainDownload

print('Welcome to your software S3 bucket assitance')

#This infinite While loop asks the user wether to generate or not new files with the mainGenerator() 
while True:
    try:
        option = input('Do you want to generate files ? (y/n): ').upper()
        if option not in ['Y', 'N']:
            print("Error: Please choose an option (y/n)")
        elif option == 'Y':
            mainGenerator()
        else:
            break
    except ValueError as e:
        print(f"Error: {e}")

#Next is another infinite While loop similar to the previous one but instead use the mainUpload() 
while True:
    try:
        option = input('Do you want to upload these files to the S3 bucket? (y/n): ').upper()
        if option not in ['Y', 'N']:
            print("Error: Please choose an option (y/n)")
        elif option == 'Y':
            mainUpload()
        else:
            break
    except ValueError as e:
        print(f"Error: {e}")

#Finally, the last infinite While loop allows the user to download the processed files locally by using the function mainDownload() 
while True:
    try:
        option = input('Do you want to download the files from your S3 bucket? (y/n): ').upper()

        if option not in ['Y', 'N']:
            print("Error: Please choose an option (y/n)")
        elif option == 'Y':
            mainDownload()
        else:
            break
    except ValueError as e:
        print(f"Error: {e}")